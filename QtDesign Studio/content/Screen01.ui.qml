/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick
import QtQuick.Controls
import UntitledProject2

Rectangle {
    id: rectangle1
    width: Constants.width
    height: Constants.height
    color: "#95bcff"
    border.color: "#cc000000"
    border.width: 0


    Image {
        id: image
        x: 62
        y: 102
        width: 100
        height: 100
        source: "../images/selectfiles.jpg"
        fillMode: Image.PreserveAspectFit
    }

    Image {
        id: image1
        x: 200
        y: 102
        width: 100
        height: 100
        source: "../images/decode.jpg"
        fillMode: Image.PreserveAspectFit
    }

    Image {
        id: image2
        x: 336
        y: 102
        width: 100
        height: 100
        source: "../images/decode.jpg"
        fillMode: Image.PreserveAspectFit
    }

    Image {
        id: image3
        x: 472
        y: 102
        width: 100
        height: 100
        source: "../images/exit.jpg"
        fillMode: Image.PreserveAspectFit
    }

    Button {
        id: button
        x: 57
        y: 208
        text: qsTr("Select Files")
    }

    Button {
        id: button1
        x: 209
        y: 208
        text: qsTr("Encode")
    }

    Button {
        id: button2
        x: 347
        y: 208
        text: qsTr("Decode")
    }

    Rectangle {
        id: rectangle
        x: 209
        y: 35
        width: 232
        height: 33
        color: "#b0cdff"
        radius: 12
        border.color: "#47000000"
        border.width: 0
    }

    Button {
        id: button3
        x: 490
        y: 208
        text: qsTr("Exit")
    }

    Label {
        id: label
        x: 242
        y: 41
        width: 166
        height: 24
        color: "#d8000000"
        text: qsTr(" File Compressor Pzyp")
        horizontalAlignment: Text.AlignHCenter
        layer.enabled: false
        font.pointSize: 15
    }


}


