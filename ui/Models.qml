import QtQuick
import QtQuick.Controls

Item {
    id: root
    property alias daysModel : daysModel
    property alias monthsModel : monthsModel
    property alias dayTimeModel : dayTimeModel
    property alias frcModel : frcModel
    property alias schoolHolidayModel : schoolHolidayModel
    property alias publicHolidayModel : publicHolidayModel
    property alias timeSetsAmModel: timeSetsAmModel
    property alias timeSetsPmModel: timeSetsPmModel
    property alias classificationModel: classificationModel
    property alias sampleSizeSearchModel: sampleSizeSearchModel
    property bool initialState: true

    ListModel {
        id: daysModel
        ListElement {
            text: 'Monday'
            checked: true
        }
        ListElement {
            text: 'Tuesday'
            checked: true
        }
        ListElement {
            text: 'Wednesday'
            checked: true
        }
        ListElement {
            text: 'Thursday'
            checked: true
        }
        ListElement {
            text: 'Friday'
            checked: true
        }
        ListElement {
            text: 'Saturday'
            checked: true
        }
        ListElement {
            text: 'Sunday'
            checked: true
        }
    }


    ListModel {
        id: monthsModel
        ListElement {
            text: 'January'
            checked: true
        }
        ListElement {
            text: 'February'
            checked: true
        }
        ListElement {
            text: 'March'
            checked: true
        }
        ListElement {
            text: 'April'
            checked: true
        }
        ListElement {
            text: 'May'
            checked: true
        }
        ListElement {
            text: 'June'
            checked: true
        }
        ListElement {
            text: 'July'
            checked: true
        }
        ListElement {
            text: 'August'
            checked: true
        }
        ListElement {
            text: 'September'
            checked: true
        }
        ListElement {
            text: 'October'
            checked: true
        }
        ListElement {
            text: 'November'
            checked: true
        }
        ListElement {
            text: 'December'
            checked: true
        }
    }

    ListModel {
        id: dayTimeModel
        ListElement {
            text: 'AM'
            checked: true
        }
        ListElement {
            text: 'PM'
            checked: true
        }
    }

    ListModel {
        id: publicHolidayModel
        ListElement {
            text: 'New Year Holidays 2022'
            checked: false
        }
        ListElement {
            text: 'Auckland Anniversary 2023'
            checked: false
        }

        ListElement {
            text: 'Waitangi Day 2023'
            checked: false
        }

        ListElement {
            text: 'Good Friday-Easter Monday'
            checked: false
        }

        ListElement {
            text: 'ANZAC Day'
            checked: false
        }

        ListElement {
            text: 'King\'s Birthday'
            checked: false
        }

        ListElement {
            text: 'Matariki'
            checked: false
        }

        ListElement {
            text: 'Labour Day'
            checked: false
        }


        ListElement {
            text: 'New Year Holidays 2023'
            checked: false
        }
    }

    ListModel {
        id: schoolHolidayModel
        ListElement {
            text: 'Term 4 Holidays, 2022'
            checked: false
        }
        ListElement {
            text: 'Term 1 Holidays, 2023'
            checked: false
        }

        ListElement {
            text: 'Term 2 Holidays, 2023'
            checked: false
        }

        ListElement {
            text: 'Term 3 Holidays, 2023'
            checked: false
        }

        ListElement {
            text: 'Term 4 Holidays, 2023'
            checked: false
        }

        ListElement {
            text: 'School start Term 1, 2023'
            checked: false
        }

        ListElement {
            text: 'School start Term 2, 2023'
            checked: false
        }

        ListElement {
            text: 'School start Term 4, 2023'
            checked: false
        }
    }

    ListModel {
        id: frcModel
        ListElement {
            text: 'FRC type: 0'
            checked: true
        }
        ListElement {
            text: 'FRC type: 1'
            checked: true
        }
        ListElement {
            text: 'FRC type: 2'
            checked: true
        }

        ListElement {
            text: 'FRC type: 3'
            checked: true
        }

        ListElement {
            text: 'FRC type: 4'
            checked: true
        }

        ListElement {
            text: 'FRC type: 5'
            checked: true
        }

        ListElement {
            text: 'FRC type: 6'
            checked: true
        }

        ListElement {
            text: 'FRC type: 7'
            checked: true
        }

        ListElement {
            text: 'FRC type: 8'
            checked: true
        }
    }

    ListModel {
        id: timeSetsAmModel
        ListElement {
            text: '5:00-5:15'
            checked: true
        }

        ListElement {
            text: '5:15-5:30'
            checked: true
        }

        ListElement {
            text: '5:30-5:45'
            checked: true
        }

        ListElement {
            text: '5:45-6:00'
            checked: true
        }

        ListElement {
            text: '6:00-6:15'
            checked: true
        }

        ListElement {
            text: '6:15-6:30'
            checked: true
        }

        ListElement {
            text: '6:30-6:45'
            checked: true
        }

        ListElement {
            text: '6:45-7:00'
            checked: true
        }

        ListElement {
            text: '7:00-7:15'
            checked: true
        }
        ListElement {
            text: '7:15-7:30'
            checked: true
        }
        ListElement {
            text: '7:30-7:45'
            checked: true
        }
        ListElement {
            text: '7:45-8:00'
            checked: true
        }
        ListElement {
            text: '8:00-8:15'
            checked: true
        }
        ListElement {
            text: '8:15-8:30'
            checked: true
        }
        ListElement {
            text: '8:30-8:45'
            checked: true
        }
        ListElement {
            text: '8:45-9:00'
            checked: true
        }
        ListElement {
            text: '9:00-9:15'
            checked: true
        }
        ListElement {
            text: '9:15-9:30'
            checked: true
        }
        ListElement {
            text: '9:30-9:45'
            checked: true
        }
        ListElement {
            text: '9:45-10:00'
            checked: true
        }
    }

    ListModel {
        id: timeSetsPmModel
        ListElement {
            text: '14:00-14:15'
            checked: true
        }

        ListElement {
            text: '14:15-14:30'
            checked: true
        }

        ListElement {
            text: '14:30-14:45'
            checked: true
        }

        ListElement {
            text: '14:45-15:00'
            checked: true
        }

        ListElement {
            text: '15:00-15:15'
            checked: true
        }

        ListElement {
            text: '15:15-15:30'
            checked: true
        }

        ListElement {
            text: '15:30-15:45'
            checked: true
        }

        ListElement {
            text: '15:45-16:00'
            checked: true
        }

        ListElement {
            text: '16:00-16:15'
            checked: true
        }
        ListElement {
            text: '16:15-16:30'
            checked: true
        }
        ListElement {
            text: '16:30-16:45'
            checked: true
        }
        ListElement {
            text: '16:45-17:00'
            checked: true
        }
        ListElement {
            text: '17:00-17:15'
            checked: true
        }
        ListElement {
            text: '17:15-17:30'
            checked: true
        }
        ListElement {
            text: '17:30-17:45'
            checked: true
        }
        ListElement {
            text: '17:45-18:00'
            checked: true
        }
        ListElement {
            text: '18:00-18:15'
            checked: true
        }
        ListElement {
            text: '18:15-18:30'
            checked: true
        }
        ListElement {
            text: '18:30-18:45'
            checked: true
        }
        ListElement {
            text: '18:45-19:00'
            checked: true
        }
    }


    ListModel {
        id: classificationModel
        ListElement {
            text: 'Peak hour similarity'
            checked: true
        }

        ListElement {
            text: 'Peak period 1 hour A'
            checked: true
        }

        ListElement {
            text: 'Peak period 2 hour A'
            checked: true
        }

        ListElement {
            text: 'Peak period 1 hour B'
            checked: true
        }
    }

    ListModel
    {
        id:sampleSizeSearchModel
        ListElement {
            text: 'Peak hour'
            checked: true
        }

        ListElement {
            text: 'Time sets'
            checked: true
        }
    }
}
