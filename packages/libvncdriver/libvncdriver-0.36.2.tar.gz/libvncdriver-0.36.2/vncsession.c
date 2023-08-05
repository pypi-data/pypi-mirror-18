// vncsession.c - VNCSession class
// https://docs.python.org/2/extending/newtypes.html

#include <stdio.h>
#include <errno.h>
#include <string.h>

// Python Headers
#include <Python.h>
#include "structmember.h"

// Needed to access numpy array functionality from other C files
// http://docs.scipy.org/doc/numpy/reference/c-api.array.html#c.NO_IMPORT_ARRAY
#define NO_IMPORT_ARRAY
#define PY_ARRAY_UNIQUE_SYMBOL libvncdriver_ARRAY_API
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include "numpy/arrayobject.h"

// libVNC Headers
#include <rfb/rfbclient.h>

// local headers
#include "logger.h"
#include "vncsession.h"

#define ARRAY_SIZE(a) (sizeof(a)/sizeof((a)[0]))

#define DEFAULT_ENCODING "zrle"

// TODO: make this initialization arg?
#define PASSWORD "openai"

// In-memory frame parameters
#define BITS_PER_SAMPLE   8  // 8-bit color
#define SAMPLES_PER_PIXEL 3  // Red, Green, Blue
#define BYTES_PER_PIXEL   4  // Each pixel is 4-byte aligned

/* Protocol extension to set subsampling */

// rfbEncodingSubsamp4X, rfbEncodingSubsamp2X, rfbEncodingSubsampGray // not implemented rfbEncodingSubsamp8X, rfbEncodingSubsamp16X
static int subsampRegistered = 0;
static int tightSubsampLevel[] = { rfbEncodingSubsamp1X, 0 };
static rfbClientProtocolExtension tightSubsampPsuedoEncoding = {
	tightSubsampLevel,		/* encodings */
	NULL,				/* handleEncoding */
	NULL,                           /* handleMessage */
	NULL				/* next extension */
};

/* Uses a hack to globally set the subsample level */
static void set_subsamp_level(int *i) {
  if (*i < 0) {
    logger_str(WARNING, "Requested subsample value of %d, but only supported are 0 (no subsample)-3 (grayscale). Using 0 instead", *i);
    *i = 0;
  } else if (*i > 3) {
    logger_str(WARNING, "Requested subsample value of %d, but only supported are 0 (no subsample)-3 (grayscale). Using 3 instead", *i);
    *i = 3;
  }

  tightSubsampLevel[0] = *i + rfbEncodingSubsamp1X;

  if (!subsampRegistered) {
    subsampRegistered = 1;
    rfbClientRegisterExtension(&tightSubsampPsuedoEncoding);
  }
}

static int fineQualityRegistered = 0;
static int fineQualityLevel[] = { rfbEncodingFineQualityLevel0, 0 };
static rfbClientProtocolExtension fineQualityPsuedoEncoding = {
        fineQualityLevel,		/* encodings */
	NULL,				/* handleEncoding */
	NULL,                           /* handleMessage */
	NULL				/* next extension */
};

/* Uses a hack to globally set the fine quality level */
static void set_fine_quality_level(int *i) {
  if (*i < 1) {
    logger_str(WARNING, "Requested fine quality value of %d, but only supported are 1 (worst)-100 (best). Using 0 instead", *i);
    *i = 1;
  } else if (*i > 100) {
    logger_str(WARNING, "Requested fine quality value of %d, but only supported are 1 (worst)-100 (best). Using 100 instead", *i);
    *i = 100;
  }

  fineQualityLevel[0] = *i + rfbEncodingFineQualityLevel0;

  if (!fineQualityRegistered) {
    fineQualityRegistered = 1;
    rfbClientRegisterExtension(&fineQualityPsuedoEncoding);
  }
}

/* Python VNC session code */

typedef struct {
  PyObject_HEAD
  /* Type-specific fields go here. */
  PyObject *remotes;
  PyObject *error_buffer;
  rfbClient *rfb_client;
  int num_updates;
} VNCSession;

static void VNCSession_dealloc(VNCSession* self) {
    Py_XDECREF(self->remotes);
    Py_XDECREF(self->error_buffer);
    if (self->rfb_client)
      rfbClientCleanup(self->rfb_client);
#if PY_MAJOR_VERSION >= 3
    Py_TYPE(self)->tp_free((PyObject*)self);
#else
    self->ob_type->tp_free((PyObject*)self);
#endif
}

// Needs to malloc memory, because libvncserver will free it after use
static char *password(rfbClient *client) {
  char *pass = (char*)malloc(sizeof(PASSWORD));
  strcpy(pass, PASSWORD);
  return pass;
}

//static void got_update(rfbClient *client, int x, int y, int w, int h) {
static void got_update(rfbClient *client) {
  VNCSession *self = (VNCSession*)rfbClientGetClientData(client, client);
  //logger_str(INFO, "Got update area %d,%d  %d*%d=%d", x, y, w, h, w * h);
  self->num_updates += 1;
}

static int VNCSession_init(VNCSession *self, PyObject *args, PyObject *kwds) {
  PyObject *remotes, *error_buffer;
  char *encoding = NULL;
  int fine_quality_level = 100, compress_level = 0, subsample_level = 0;

  char *hostport;
  char hostbuf[1024] = {0};
  char *host = NULL;
  int port;

  static char *kwlist[] = {"remotes", "error_buffer", "encoding", "fine_quality_level", "compress_level", "subsample_level", NULL};

  error_buffer = &_Py_NoneStruct;
  if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|Osiii", kwlist, &remotes, &error_buffer, &encoding, &fine_quality_level, &compress_level, &subsample_level))
      return -1;

  if (!PyList_Check(remotes)) {
    PyErr_SetString(PyExc_TypeError, "remotes must be called with list of remotes (with one entry for now)");
    return -1;
  }

  // Currently we only send single-item lists, just get the first item
  remotes = PyList_GetItem(remotes, 0);
  if (remotes == NULL) {
    return -1;
  }

  // python: self.remotes = remotes
  Py_INCREF(remotes);
  self->remotes = remotes;
  // python: self.error_buffer = error_buffer
  Py_INCREF(error_buffer);
  self->error_buffer = error_buffer;

  PyObject* unicode_remotes = PyUnicode_FromObject(remotes);
  if(unicode_remotes == NULL)
  {
    return -1;
  }

  PyObject* ascii_remotes = PyUnicode_AsASCIIString(unicode_remotes);

  if(ascii_remotes == NULL)
  {
    return -1;
  }
  // python: hostport = str(remotes)
  hostport = PyBytes_AsString(ascii_remotes);
  if (hostport == NULL) {
    return -1;
  }

  // build encoding if we didn't get any
  if (encoding == NULL) {
    encoding = (char*)malloc(sizeof(DEFAULT_ENCODING));
    strcpy(encoding, DEFAULT_ENCODING);
  }

  // Parse "host:port" into separated host and port
  if (sscanf(hostport, "%[^:]:%d", &hostbuf, &port) < 2) {
    logger_str(ERROR, "Failed to parse %s into host %s port %d", hostport, hostbuf, port);
    return -1;
  }

  // rfbClientCleanup will free this, so we have to malloc it
  host = (char*)malloc(sizeof(hostbuf));
  strcpy(host, hostbuf);

  self->rfb_client = rfbGetClient(BITS_PER_SAMPLE, SAMPLES_PER_PIXEL, BYTES_PER_PIXEL);
  self->rfb_client->FinishedFrameBufferUpdate = got_update;
  self->rfb_client->GetPassword = password;
  self->rfb_client->appData.encodingsString = encoding;
  self->rfb_client->appData.useRemoteCursor = FALSE;

  // Even though 0-9 are the valid values, in practice we really want
  // to use a subset. The server will translate values outside that
  // range. See:
  // 
  // https://github.com/TurboVNC/turbovnc/blob/master/unix/Xvnc/programs/Xserver/hw/vnc/tight.c#L249-L286
  if (compress_level > 9) {
    logger_str(WARNING, "Requested compress_level value of %d, but only supported are 0 (minimal)-9 (maximal). Using 9 instead", compress_level);
    compress_level = 9;
  } else if (compress_level < 0) {
    logger_str(WARNING, "Requested compress_level value of %d, but only supported are 0 (minimal)-9 (maximal). Using 0 instead", compress_level);
    compress_level = 0;
  }
  self->rfb_client->appData.compressLevel = compress_level; 

  // Don't use libvncserver's native quality level, since it's less
  // fine-grained than TurboVNC supports.  TurboVNC translates it to a
  // combination of compress and fine quality levels. (cf
  // https://github.com/TurboVNC/turbovnc/blob/master/unix/Xvnc/programs/Xserver/hw/vnc/rfbserver.c#L1103-L1114)
  //
  // self->rfb_client->appData.qualityLevel = quality_level;
  //
  // Similarly, we set the quality levels ourselves, and thus disable libvncserver's enableJPEG
  self->rfb_client->appData.enableJPEG = FALSE;

  /* 1 (worst)-100 (best) */
  set_fine_quality_level(&fine_quality_level);
  /* 
     0: 1x [normal]
     1: 4x
     2: 2x
     3: Grayscale
     4: 8x
     5: 16x
  */
  set_subsamp_level(&subsample_level);
  self->rfb_client->serverHost = host;
  self->rfb_client->serverPort = port;

  logger_str(INFO, "Establish VNC session with: encoding=%s fine_quality_level=%d compress_level=%d subsample_level=%d", encoding, fine_quality_level, compress_level, subsample_level);
  SetFormatAndEncodings(self->rfb_client);

  strcpy(last_log, "(no error logged)");
  if (!rfbInitClient(self->rfb_client, NULL, NULL)) {
    self->rfb_client = NULL;
    PyErr_Format(PyExc_Exception, "Error in rfbInitClient: %s", last_log);
    return -1;
  }

  // Store a reference to self we can access from the rfbclient methods
  rfbClientSetClientData(self->rfb_client, self->rfb_client, self);
  return 0;
}

PyMemberDef VNCSession_members[] = {
  {"remotes", T_OBJECT_EX, offsetof(VNCSession, remotes), READONLY,
    "VNC remotes to connect to"},
  {"error_buffer", T_OBJECT_EX, offsetof(VNCSession, error_buffer), 0,
    "Asynchronous error buffer"},
  {NULL} /* Sentinel */
};

static PyObject *VNCSession_close(VNCSession *self) {
  logger_str(INFO, "closing VNCSession connections");
  if (self->rfb_client)
    rfbClientCleanup(self->rfb_client);
  Py_RETURN_NONE;
 }

// Send a key event to the vnc server
// Return negative on failure, with exception set; otherwise return 0
static int send_key(rfbClient *client, PyObject *key, PyObject *down) {
  long key_val = PyLong_AsLong(key);
  int down_val = PyObject_IsTrue(down);
  if (PyErr_Occurred()) {
    return -1;
  }

  strcpy(last_log, "(no error logged)");
  if (!SendKeyEvent(client, key_val, down_val)) {
    PyErr_Format(PyExc_Exception, "Error in SendKeyEvent: failure: %s", last_log);
    return -1;
  }
  return 0;
}

// Send a pointer event to the vnc server
// Return negative on failure, with exception set; otherwise return 0
static int send_point(rfbClient *client, PyObject *x, PyObject *y, PyObject *buttonmask) {
  long x_val = PyLong_AsLong(x);
  long y_val = PyLong_AsLong(y);
  long buttonmask_val = PyLong_AsLong(buttonmask);
  if (PyErr_Occurred()) {
    return -1;
  }

  strcpy(last_log, "(no error logged)");
  if (!SendPointerEvent(client, x_val, y_val, buttonmask_val)) {
    PyErr_Format(PyExc_Exception, "Error in SendPointerEvent: failure: %s", last_log);
    return -1;
  }
  return 0;
}

// Process a single event tuple to send to the vnc server
// Return negative on failure, with exception set; otherwise return 0
static int send_event(rfbClient *client, PyObject *event) {
  char *event_type = PyBytes_AsString(PyUnicode_AsASCIIString(PyUnicode_FromObject(PyTuple_GetItem(event, 0))));
  if (event_type == NULL) {
    return -1;
  }

  if (!strcmp(event_type, "KeyEvent")) {  // (key, down)
    return send_key(client, PyTuple_GetItem(event, 1), PyTuple_GetItem(event, 2));
  } else if (!strcmp(event_type, "PointerEvent")) {  // (x, y, buttonmask)
    return send_point(client, PyTuple_GetItem(event, 1), PyTuple_GetItem(event, 2), PyTuple_GetItem(event, 3));
  }
  PyErr_Format(PyExc_Exception, "Invalid event type: %s", event_type);
  return -1;
}

// send a single event to the vnc server
static PyObject *VNCSession_event(VNCSession *self, PyObject *arg) {
  if (send_event(self->rfb_client, arg) < 0) {
    return NULL;
  }
  Py_RETURN_NONE;
}

// Handle RFB Messages from the Server, including applying framebuffer updates
// Returns -1 on failure, and sets python exception; otherwise returns 0
static int flip(rfbClient *client) {
  int i;
  while ((i = WaitForMessage(client, 0))) {
    if (i < 0) {
      PyErr_Format(PyExc_Exception, "Error in WaitForMessage: %d (%s)", errno, strerror(errno));
      return -1;
    }

    if (i > 0) {
      strcpy(last_log, "(no error logged)");
      if(!HandleRFBServerMessage(client)) {
	PyErr_Format(PyExc_Exception, "Error in HandleRFBServerMessage: %s", last_log);
        return -1;
      }
    }
  }

  return 0;
}

// Create a new numpy array with existing frame data, and return it
// Return NULL on failure, otherwise returns numpy array object
static PyObject *array(rfbClient *client) {
  npy_intp dims[] = {client->height, client->width, SAMPLES_PER_PIXEL};
  npy_intp strides[] = {BYTES_PER_PIXEL * client->width, BYTES_PER_PIXEL, 1};
  PyObject *array = PyArray_New(&PyArray_Type, SAMPLES_PER_PIXEL, dims,
                                NPY_UINT8, strides, client->frameBuffer, -1,
                                NPY_ARRAY_CARRAY, NULL);
  if (!array) {
    return NULL;
  }
  Py_INCREF(array);
  return array;
}

// Flips and returns frame, n_updates
static PyObject *VNCSession_flip(VNCSession *self) {
  PyObject *dict, *n_updates;
  self->num_updates = 0;
  if (flip(self->rfb_client) < 0) {
    return NULL;
  }
  // Build dict for num_updates
  dict = PyDict_New();
  if (dict == NULL) {
    return NULL;
  }
  n_updates = PyLong_FromLong(self->num_updates);
  if (n_updates == NULL) {
    return NULL;
  }
  if (PyDict_SetItemString(dict, "vnc.updates.n", n_updates) < 0) {
    PyErr_SetString(PyExc_Exception, "Failed to add vnc.updates.n to dict");
    return NULL;
  }
  return Py_BuildValue("([O][O])", array(self->rfb_client), dict);
}

// takes a list of lists of events to send, and returns frame, n_updates
static PyObject *VNCSession_step(VNCSession *self, PyObject *arg) {
  // Currently we only send single-item lists, just get the first item
  PyObject *events = PyList_GetItem(arg, 0);

  if (!PyList_Check(events)) {
    PyErr_SetString(PyExc_TypeError, "Step must be called with list of list");
    return NULL;
  }

  // Iterate through (inner) list of events, handling each one
  PyObject *item, *iterator = PyObject_GetIter(events);
  while ((item = PyIter_Next(iterator))) {
    if (send_event(self->rfb_client, item) < 0) {
      Py_DECREF(item);  // still have a reference in this case
      break;  // If we hit an exception handling one, bail immediately
    }
    Py_DECREF(item);
  }
  Py_XDECREF(iterator);

  if (PyErr_Occurred()) {
    return NULL;
  }

  return VNCSession_flip(self);
}

PyMethodDef VNCSession_methods[] = {
  {"close", (PyCFunction)VNCSession_close, METH_NOARGS, "Close VNC connection"},
  {"flip", (PyCFunction)VNCSession_flip, METH_NOARGS, "Flip most recent frame"},
  {"step", (PyCFunction)VNCSession_step, METH_O, "Perform actions and then flip"},
  {"event", (PyCFunction)VNCSession_event, METH_O, "Send a single event"},
  {NULL} /* Sentinel */
};

// Note: the way these are usually initialized is pretty gross
PyTypeObject VNCSession_type = {
  .tp_name = "libvncdriver.VNCSession",
  .tp_basicsize = sizeof(VNCSession),
  .tp_dealloc = (destructor)VNCSession_dealloc,
  .tp_flags = Py_TPFLAGS_DEFAULT,
  .tp_doc = "VNC Session class",
  .tp_new = PyType_GenericNew,
  .tp_init = (initproc)VNCSession_init,
  .tp_methods = VNCSession_methods,
  .tp_members = VNCSession_members,
};

#define MAX_LOGGER_ARGS 1024

int libvncdriver_init() {
  rfbClientLog = logger_str_info_chomp;
  rfbClientErr = logger_str_error_chomp;
  return 0;
}
