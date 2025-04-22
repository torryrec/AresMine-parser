# AresMine-parser
Description:
This Python application is a real-time monitoring tool that tracks the latest 5 orders from the official Aresmine Minecraft marketplace (https://aresmine.ru/). The program checks the Aresmine API every 30 seconds, displaying new orders in a user-friendly terminal interface while avoiding duplicate entries.

Key Features:

    Real-time monitoring of Aresmine marketplace transactions

    Automatic duplicate detection (unique usernames)

    Terminal-based interface with scrollable history

    Persistent logging to output.txt

    Start/Stop control without exiting the program

    Error handling and connection timeout management

Data Source:
The application retrieves order information from the official Aresmine API endpoint:
https://api.aresmine.ru/orders/last/5

All data is obtained directly from Aresmine's servers and includes:

    Username of purchaser

    Product name purchased

    Payment status/amount

Technical Specifications:

    Built with Python 3.x

    Uses Textual for terminal UI (TUI)

    Requires only requests and textual packages

    Thread-safe implementation

    Lightweight (under 2MB memory usage)

Usage Instructions:

    Run the program in any terminal

    Press [Start] to begin monitoring

    View real-time updates in the scrollable window

    Press [Stop] to pause monitoring

    Press [Q] or Ctrl+C to exit

Note:
This is an unofficial monitoring tool. Aresmine is a registered trademark of its respective owners. The developer of this tool is not affiliated with Aresmine.ru. All order data remains property of Aresmine and is used in accordance with their public API availability.

This description maintains professional tone while:

    Clearly stating the data source

    Explaining functionality

    Including disclaimer about unofficial status

    Providing technical details

    Offering clear usage instructions
