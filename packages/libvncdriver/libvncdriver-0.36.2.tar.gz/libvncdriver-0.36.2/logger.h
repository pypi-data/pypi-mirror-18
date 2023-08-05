// logger.h - hook into python's logging module

#include <stdarg.h>

// https://docs.python.org/2.7/library/logging.html#logging-levels
typedef enum {
  NOTSET = 0,
  DEBUG = 10,
  INFO = 20,
  WARNING = 30,
  ERROR = 40,
  CRITICAL = 50,
} logging_level_e;

// Call once to initialize and setup logging
// Returns negative on failure
int logger_init(void);

// Use the python logger to log a string (printf-style)
void logger_str(logging_level_e level, const char *format, ...);
// Use the python logger to log a string at a fixed variant
void logger_str_info_chomp(const char *format, ...);
void logger_str_error_chomp(const char *format, ...);

// Shared between the two chomp methods
char last_log[4096];
