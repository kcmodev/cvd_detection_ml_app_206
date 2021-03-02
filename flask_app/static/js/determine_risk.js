document.getElementById("submitDataButton").addEventListener('click', submitUserInput);

function submitUserInput() {
    let userAgeInDays;
    let todaysDateDays;
    let bday = document.getElementById("ageInput").value;

    bday = Date.parse(bday);
    bday = (bday / (60 * 60 * 24 * 1000));

    todaysDateDays = Date.now();
    todaysDateDays = (todaysDateDays / (60 * 60 * 24 * 1000));

    userAgeInDays = todaysDateDays - bday;

    let height = document.getElementById("heightInput").value;
    let weight = document.getElementById("weightInput").value;

    let gender;
    if (document.getElementById("maleSelected").checked){
        gender = 2;
    } else if (document.getElementById("femaleSelected").checked) {
        gender = 1;
    }

    let systolic_bp = document.getElementById("systolic_bp").value;
    let diastolic_bp = document.getElementById("diastolic_bp").value;
    let blood_glucose = document.getElementById("glucoseDropdownSelect").value;
    let cholesterol = document.getElementById("cholesterolDropdownSelect").value;

    let alcohol_intake;
    if (document.getElementById("yesAlcoholUse").checked) {
        alcohol_intake = 1
    } else if (document.getElementById("noAlcoholUse").checked) {
        alcohol_intake = 0
    }

    let current_smoker;
    if (document.getElementById("isASmoker").checked) {
        current_smoker = 1
    } else if (document.getElementById("notASmoker").checked) {
        current_smoker = 0
    }

    let physically_active;
    if (document.getElementById("yesActivity").checked) {
        physically_active = 1
    } else if (document.getElementById("noActivity").checked) {
        physically_active = 0
    }

    let allData = [
        {"age": userAgeInDays},
        {"height": height},
        {"weight": weight},
        {"gender": gender},
        {"systolic_bp": systolic_bp},
        {"diastolic_bp": diastolic_bp},
        {"blood_glucose": blood_glucose},
        {"cholesterol": cholesterol},
        {"alcohol_intake": alcohol_intake},
        {"current_smoker": current_smoker},
        {"physically_active": physically_active}
        ];

    // console.log(`Data being sent: ${allData}`)
    console.log(`Data being sent as JSON: ${JSON.stringify(allData)}`)
    sendResults(allData)
}

function sendResults(data) {
    $.ajax({
        type: "POST",
        url: "/calculated_risk_results",
        dataType: "json",
        data: JSON.stringify(data),
        contentType: 'application/json',

        success: function (data) {
            console.log(`Post of \"${data}\" sent successfully`)

        console.log('sending GET request')
        $.ajax({
            type: "GET",
            data: data,

            success: function (){
                window.location.href = 'calculated_risk_results';
            }
        });

        }
    });
}