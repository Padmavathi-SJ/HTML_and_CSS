--> onopen callback: Executes when connection is established

Timeline:
1. User clicks Join button
2. Browser attempts connections
3. Server sccepts connection (handshake)
4. onopen fires
5. Send "join" message to server
   
# Auto-Scroll Feature
chat.scrollTop = chat.scrollHeight

what it does
--> scrollTop = vertical scroll position (0 = top)
--> scrollHeight = Total height of the conect
--> setting scrollTop to scrollHeight = scroll to bottom
Ensures newest messages are always visible.