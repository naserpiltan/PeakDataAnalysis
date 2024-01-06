import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

ApplicationWindow {
    visible: true
    width: 800
    height: 700
    title: "HelloApp ads"
    Material.theme: Material.Dark

    HomePage
    {
        id:homePage
        anchors.fill:parent
    }

    Popup {
            id: notificationPopup
            width: 600
            height: 100
            modal: false
            visible: false
            x: 200
            y:200
            property string notificationText : ""

            Rectangle {
                width: parent.width
                height: parent.height
                color: "#3498db" // Background color for the notification

                Text {
                    anchors.centerIn: parent
                    text: notificationPopup.notificationText
                    color: "white"
                    font.pixelSize: 16
                    horizontalAlignment: Qt.AlignHCenter
                }
            }

            Behavior on opacity {
                NumberAnimation {
                    duration: 1000 // Animation duration in milliseconds
                }
            }

            onOpened: {
                // Hide the notification after a delay (e.g., 3 seconds)
                notificationTimer.start()
            }
        }

        Timer {
            id: notificationTimer
            interval: 3000 // Delay in milliseconds
            onTriggered: {
                // Close the notification popup after the delay
                notificationPopup.close()
            }
        }
}
