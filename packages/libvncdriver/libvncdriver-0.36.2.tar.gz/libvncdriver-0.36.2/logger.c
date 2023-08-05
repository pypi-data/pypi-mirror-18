// logger.c - hook into python's logging module

#include <Python.h>
#include <stdarg.h>
#include "logger.h"

static PyObject *logger;

// First-time import the logging module, or throw an exception trying
int logger_init(void) {
  PyObject *logging_module = NULL;

  // python: import logging
  if (NULL == logger) {
    logging_module = PyImport_ImportModuleNoBlock("logging");
    if (NULL == logging_module) {
      PyErr_SetString(PyExc_ImportError, "Failed to import 'logging' module");
      return -1;
    }
  }

  // python: logging.basicConfig()
  PyObject_CallMethod(logging_module, "basicConfig", NULL);
  // python: logger = logging.getLogger('libvncdriver')
  logger = PyObject_CallMethod(logging_module, "getLogger", "s", "libvncdriver");
  // python: logger.setLevel(INFO)
  PyObject_CallMethod(logger, "setLevel", "i", INFO);

  return 0;
}

void logger_str(logging_level_e level, const char *format, ...) {
  char buf[1024];  // Should be enough for anybody...
  va_list(args);
  va_start(args, format);
  vsnprintf(buf, sizeof(buf), format, args);
  va_end(args);
  PyObject_CallMethod(logger, "log", "ls", (long)level, buf);
}

// We need these for rfbLog, and there's not a good way to delegate varargs

void logger_str_info_chomp(const char *format, ...) {
  char *copy = NULL;
  if (format[strlen(format)-1] == '\n') {
    // Strip off the trailing newline
    copy = malloc(strlen(format));
    strncpy(copy, format, strlen(format)-1);
    copy[strlen(format)-1] = '\0';
    format = copy;
  }

  va_list(args);
  va_start(args, format);
  vsnprintf(last_log, sizeof(last_log), format, args);
  va_end(args);

  PyObject_CallMethod(logger, "log", "ls", (long)INFO, last_log);

  if (copy != NULL)
    free(copy);
}

void logger_str_error_chomp(const char *format, ...) {
  char *copy = NULL;
  if (format[strlen(format)-1] == '\n') {
    // Strip off the trailing newline
    copy = malloc(strlen(format));
    strncpy(copy, format, strlen(format)-1);
    copy[strlen(format)-1] = '\0';
    format = copy;
  }

  va_list(args);
  va_start(args, format);
  vsnprintf(last_log, sizeof(last_log), format, args);
  va_end(args);

  PyObject_CallMethod(logger, "log", "ls", (long)ERROR, last_log);

  if (copy != NULL)
    free(copy);
}
