import QtQuick.Layouts
import QtQuick
import QtQuick.Controls

ComboBox
{
    id:daysComboBox
    currentIndex : 0
    signal indexValueChanged(int index, bool value)
    delegate: CheckableItem
    {
        width: daysComboBox.width
        text: model.text
        checked: model.checked
        index: model.index
        height: daysComboBox.height
    }
}



