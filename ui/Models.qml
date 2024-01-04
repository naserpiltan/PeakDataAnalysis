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

    ListModel {
        id: daysModel
        ListElement {
            text: 'Monday'
            checked: false
        }
        ListElement {
            text: 'Tuesday'
            checked: false
        }
        ListElement {
            text: 'Wednesday'
            checked: false
        }
        ListElement {
            text: 'Thursday'
            checked: false
        }
        ListElement {
            text: 'Friday'
            checked: false
        }
        ListElement {
            text: 'Saturday'
            checked: false
        }
        ListElement {
            text: 'Sunday'
            checked: false
        }
    }


    ListModel {
        id: monthsModel
        ListElement {
            text: 'January'
            checked: false
        }
        ListElement {
            text: 'February'
            checked: false
        }
        ListElement {
            text: 'March'
            checked: false
        }
        ListElement {
            text: 'April'
            checked: false
        }
        ListElement {
            text: 'May'
            checked: false
        }
        ListElement {
            text: 'June'
            checked: false
        }
        ListElement {
            text: 'July'
            checked: false
        }
        ListElement {
            text: 'August'
            checked: false
        }
        ListElement {
            text: 'September'
            checked: false
        }
        ListElement {
            text: 'October'
            checked: false
        }
        ListElement {
            text: 'November'
            checked: false
        }
        ListElement {
            text: 'December'
            checked: false
        }
    }

    ListModel {
        id: dayTimeModel
        ListElement {
            text: 'AM'
            checked: false
        }
        ListElement {
            text: 'PM'
            checked: false
        }
    }

    ListModel {
        id: publicHolidayModel
        ListElement {
            text: 'Christmass Day 2022'
            checked: false
        }
        ListElement {
            text: 'Boxing Day 2022'
            checked: false
        }

        ListElement {
            text: 'New Year Day'
            checked: false
        }

        ListElement {
            text: 'Day after New Year Day'
            checked: false
        }

        ListElement {
            text: 'Aukland Anniversary'
            checked: false
        }

        ListElement {
            text: 'Waitangi Day'
            checked: false
        }

        ListElement {
            text: 'Good Friday'
            checked: false
        }

        ListElement {
            text: 'Easter Monday'
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
            text: 'labour Day'
            checked: false
        }

        ListElement {
            text: 'Christmass Day 2023'
            checked: false
        }
        ListElement {
            text: 'Boxing Day 2023'
            checked: false
        }

    }

    ListModel {
        id: schoolHolidayModel
        ListElement {
            text: 'Term 4, 2022'
            checked: false
        }
        ListElement {
            text: 'Summer Holidays 2022-2023'
            checked: false
        }

        ListElement {
            text: 'Term 1, 2023'
            checked: false
        }

        ListElement {
            text: 'Autumn Holidays 2023'
            checked: false
        }

        ListElement {
            text: 'Term 2, 2023'
            checked: false
        }

        ListElement {
            text: 'Winter Holidays 2023'
            checked: false
        }

        ListElement {
            text: 'Term 3, 2023'
            checked: false
        }

        ListElement {
            text: 'Spring Holidays 2023'
            checked: false
        }

        ListElement {
            text: 'Term 4, 2023'
            checked: false
        }
    }

    ListModel {
        id: frcModel
        ListElement {
            text: 'FRC type: 0'
            checked: false
        }
        ListElement {
            text: 'FRC type: 1'
            checked: false
        }
        ListElement {
            text: 'FRC type: 2'
            checked: false
        }

        ListElement {
            text: 'FRC type: 3'
            checked: false
        }

        ListElement {
            text: 'FRC type: 4'
            checked: false
        }

        ListElement {
            text: 'FRC type: 5'
            checked: false
        }

        ListElement {
            text: 'FRC type: 6'
            checked: false
        }

        ListElement {
            text: 'FRC type: 7'
            checked: false
        }

        ListElement {
            text: 'FRC type: 8'
            checked: false
        }
    }

    ListModel {
        id: timeSetsAmModel
        ListElement {
            text: '5:00-5:15'
            checked: false
        }

        ListElement {
            text: '5:15-5:30'
            checked: false
        }

        ListElement {
            text: '5:30-5:45'
            checked: false
        }

        ListElement {
            text: '5:45-6:00'
            checked: false
        }

        ListElement {
            text: '6:00-6:15'
            checked: false
        }

        ListElement {
            text: '6:15-6:30'
            checked: false
        }

        ListElement {
            text: '6:30-6:45'
            checked: false
        }

        ListElement {
            text: '6:45-7:00'
            checked: false
        }

        ListElement {
            text: '7:00-7:15'
            checked: false
        }
        ListElement {
            text: '7:15-7:30'
            checked: false
        }
        ListElement {
            text: '7:30-7:45'
            checked: false
        }
        ListElement {
            text: '7:45-8:00'
            checked: false
        }
        ListElement {
            text: '8:00-8:15'
            checked: false
        }
        ListElement {
            text: '8:15-8:30'
            checked: false
        }
        ListElement {
            text: '8:30-8:45'
            checked: false
        }
        ListElement {
            text: '8:45-9:00'
            checked: false
        }
        ListElement {
            text: '9:00-9:15'
            checked: false
        }
        ListElement {
            text: '9:15-9:30'
            checked: false
        }
        ListElement {
            text: '9:30-9:45'
            checked: false
        }
        ListElement {
            text: '9:45-10:00'
            checked: false
        }
    }

    ListModel {
        id: timeSetsPmModel
        ListElement {
            text: '14:00-14:15'
            checked: false
        }

        ListElement {
            text: '14:15-14:30'
            checked: false
        }

        ListElement {
            text: '14:30-14:45'
            checked: false
        }

        ListElement {
            text: '14:45-15:00'
            checked: false
        }

        ListElement {
            text: '15:00-15:15'
            checked: false
        }

        ListElement {
            text: '15:15-15:30'
            checked: false
        }

        ListElement {
            text: '15:30-15:45'
            checked: false
        }

        ListElement {
            text: '15:45-16:00'
            checked: false
        }

        ListElement {
            text: '16:00-16:15'
            checked: false
        }
        ListElement {
            text: '16:15-16:30'
            checked: false
        }
        ListElement {
            text: '16:30-16:45'
            checked: false
        }
        ListElement {
            text: '16:45-17:00'
            checked: false
        }
        ListElement {
            text: '17:00-17:15'
            checked: false
        }
        ListElement {
            text: '17:15-17:30'
            checked: false
        }
        ListElement {
            text: '17:30-17:45'
            checked: false
        }
        ListElement {
            text: '17:45-18:00'
            checked: false
        }
        ListElement {
            text: '18:00-18:15'
            checked: false
        }
        ListElement {
            text: '18:15-18:30'
            checked: false
        }
        ListElement {
            text: '18:30-18:45'
            checked: false
        }
        ListElement {
            text: '18:45-19:00'
            checked: false
        }
    }


    ListModel {
        id: classificationModel
        ListElement {
            text: 'Peak hour similarity'
            checked: false
        }

        ListElement {
            text: 'Peak period 1 hour A'
            checked: false
        }

        ListElement {
            text: 'Peak period 2 hour A'
            checked: false
        }

        ListElement {
            text: 'Peak period 1 hour B'
            checked: false
        }
    }

    ListModel
    {
        id:sampleSizeSearchModel
        ListElement {
            text: 'Peak hour'
            checked: false
        }

        ListElement {
            text: 'Time sets'
            checked: false
        }
    }
}
