import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

ApplicationWindow {
    visible: true
    width: 800
    height: 650
    title: "HelloApp ads"
    Material.theme: Material.Dark

    HomePage
    {
        id:homePage
        anchors.fill:parent
    }
}
