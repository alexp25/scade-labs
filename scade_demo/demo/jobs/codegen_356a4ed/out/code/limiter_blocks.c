/* $ Ansys Scade One - Swan Code Generator - Version 2.4.0 - Build 0955 
** Command: swan_cg.exe config.json -student
*************************************************************$ */
#include "swan_sensors.h"
#include "swan_consts.h"
#include "limiter_blocks.h"

/* blocks::limiter */
swan_float64 limiter_blocks(
  /* row_cmd */swan_float64 row_cmd,
  /* min */swan_float64 min,
  /* max */swan_float64 max)
{
  /* cmd */
  swan_float64 cmd;

  if (row_cmd > max) {
    cmd = max;
  }
  else if (row_cmd < min) {
    cmd = min;
  }
  else {
    cmd = row_cmd;
  }
  return cmd;
}



/* $ Ansys Scade One - Swan Code Generator - Version 2.4.0 - Build 0955 
** limiter_blocks.c
*************************************************************$ */
