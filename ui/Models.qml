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
    property alias timeSetsModel: timeSetsModel
    property alias classificationModel: classificationModel

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
            text: '1'
            checked: false
        }
        ListElement {
            text: '2'
            checked: false
        }

        ListElement {
            text: '3'
            checked: false
        }

        ListElement {
            text: '4'
            checked: false
        }

        ListElement {
            text: '5'
            checked: false
        }

        ListElement {
            text: '6'
            checked: false
        }

        ListElement {
            text: '7'
            checked: false
        }

        ListElement {
            text: '8'
            checked: false
        }

        ListElement {
            text: '9'
            checked: false
        }

        ListElement {
            text: '10'
            checked: false
        }
    }

    ListModel {
        id: timeSetsModel
        ListElement {
            text: '2'
            checked: false
        }

        ListElement {
            text: '3'
            checked: false
        }

        ListElement {
            text: '4'
            checked: false
        }

        ListElement {
            text: '5'
            checked: false
        }

        ListElement {
            text: '6'
            checked: false
        }

        ListElement {
            text: '7'
            checked: false
        }

        ListElement {
            text: '8'
            checked: false
        }

        ListElement {
            text: '9'
            checked: false
        }

        ListElement {
            text: '10'
            checked: false
        }
        ListElement {
            text: '11'
            checked: false
        }
        ListElement {
            text: '12'
            checked: false
        }
        ListElement {
            text: '13'
            checked: false
        }
        ListElement {
            text: '14'
            checked: false
        }
        ListElement {
            text: '15'
            checked: false
        }
        ListElement {
            text: '16'
            checked: false
        }
        ListElement {
            text: '17'
            checked: false
        }
        ListElement {
            text: '18'
            checked: false
        }
        ListElement {
            text: '19'
            checked: false
        }
        ListElement {
            text: '20'
            checked: false
        }
        ListElement {
            text: '21'
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
}
