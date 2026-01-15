// This module ensures that sokol and sokol_gp are implemented only once.

#define SOKOL_IMPL
#define SOKOL_GLCORE
#include "sokol_gfx.h"

#define SOKOL_LOG_IMPL
#include "sokol_log.h"

#define SOKOL_GP_IMPL
#include "sokol_gp.h"
