import QtQuick 2.0;
import calamares.slideshow 1.0;

Presentation
{
    id: presentation

    Timer {
        interval: 20000
        repeat: true
        onTriggered: presentation.goToNextSlide()
    }

    Slide {
        Image {
            id: background1
            source: "slide.png"
            width: 467
            height: 280
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
        }
        Text {
            anchors.horizontalCenter: background1.horizontalCenter
            anchors.top: background1.bottom
            text: "Installing Cyberdeck OS Beta 1 (Plow). The rest of this step is automatic."
            wrapMode: Text.WordWrap
            width: 600
            horizontalAlignment: Text.Center
            color: "#1c3a4a"
        }
    }
}
