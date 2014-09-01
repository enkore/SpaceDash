import QtQuick 2.3

Item {
    id: dashboardItem
    //signal clicked()

    //width: 40; height: 25

    Rectangle {
        id: rectangle
        border.color: "white"
        anchors.fill: parent
    }

    function updateTemperature(text){
        temperatureText.text = text
    }

    Text {
        id: temperatureText
        text: "Temperatur"
    }

    /*MouseArea {
        anchors.fill: parent
        onClicked: dashboardItem.clicked()
    }*/
}