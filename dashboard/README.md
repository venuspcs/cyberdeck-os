# dashboard/

Reserved for the Field Dashboard: a KDE Plasma desktop widget, and the drivers that feed its tiles.

When it is written, the widget will let the user add, remove, rearrange, and resize tiles, with settings saved per tile. The layout is restored at the next login.

Planned tile types:

- Internal laptop battery, when the machine has one
- External battery over Bluetooth, one tile per battery, including smart LiFePO4 and solar batteries that expose a BMS
- Solar charge controller over Bluetooth, one tile per controller
- Drive space, including the root filesystem and `/library`
- Nomad status
- Meshtastic node count
- GPS time

The first charge-controller drivers cover Victron SmartSolar over BLE, Renogy BT-1, Renogy BT-2, and EPEver. Several batteries and several controllers can be connected at the same time.

Drivers are plugins. The widget shell owns layout. A driver owns discovery and readings for one device class. A new BLE battery or charge controller is a new driver, loaded by the same shell.

**There is no widget and no driver here.** No QML, no Plasma package, and no sample device protocol. Adding those files would pretend the dashboard works.

Requirements: [docs/SPEC.md](../docs/SPEC.md), section 15.
