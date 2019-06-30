//compile with:
//gcc main.c -lX11 -o disable_pinch_zoom

#include <X11/Xlib.h>
#include <stdio.h>
#include <stdlib.h>

#define TRUE 1
#define FALSE 0

int main(int argc, char* argv[])
{
   Display* display;
   XEvent ev;
   char keymap[32];
   char Control_L_Held;
   char ALT_L_Held;
   
   display = XOpenDisplay(NULL);
   
   if (!display)
   {
      printf("Can not open display.\n");
      exit(EXIT_FAILURE);
   }

   XGrabButton(display, AnyButton, AnyModifier, DefaultRootWindow(display),
               TRUE, ButtonPressMask, GrabModeSync, GrabModeAsync, None, None);
   
   while (TRUE)
   {
      XNextEvent(display, &ev);
      
      XQueryKeymap(display, keymap);
      
      Control_L_Held = keymap[4] & (1 << 5);
      ALT_L_Held = keymap[8] & (1 << 0);
      
      if (ev.type == ButtonPress)
      {
         if ((ev.xbutton.button == 4) || (ev.xbutton.button == 5)) // mouse wheel
         {
            if (Control_L_Held)
            {
               if (ALT_L_Held) // Use 'ctrl + alt + mouse wheel' to EXIT
               break;
               
               XAllowEvents(display, AsyncPointer, ev.xbutton.time);// don't replay event
               continue;
            }
         }
         
         XAllowEvents(display, ReplayPointer, ev.xbutton.time);
      }
   }
   
   XCloseDisplay(display);
   return EXIT_SUCCESS;
}
