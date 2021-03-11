document.getElementById("submitDataButton").addEventListener('click', submitUserInput);

function submitUserInput() {
    // Takes in day, month, and year separately
    let birthdayMonth = document.getElementById("birthdateMonth").value;
    console.log(`bdayMonth: ${birthdayMonth} type: ${typeof birthdayMonth}`)
    let birthdayDay = document.getElementById("birthdateDay").value;
    console.log(`bdayDay: ${birthdayDay} type: ${typeof birthdayDay}`)
    let birthdayYear = document.getElementById("birthdateYear").value;
    console.log(`bdayYear: ${birthdayYear} type: ${typeof birthdayYear}`)

    // checks for valid days in a month
    let monthsWith30Days = [1, 3, 5, 7, 8, 10, 12]

    try {
        // checks for valid date entry such as April 31st throws an error since it is an invalid date
        if (monthsWith30Days.includes(birthdayMonth - 1)) {
            if (birthdayDay === '31') {
                throw `${birthdayMonth}/${birthdayDay}/${birthdayYear} is not a valid date. Please Try again.`;
            }
        }

        // combines variables into a date object of the users birthdate
        let fullBirthdate = new Date(birthdayYear, birthdayMonth - 1, birthdayDay);

        // determines if birth year is a leap year
        // if an invalid date is detected it alerts the user and reloads the
        if (birthdayMonth === '2') {
            if (birthdayDay === '30' || birthdayDay === '31') {
                throw `${birthdayMonth}/${birthdayDay}/${birthdayYear} is not a valid date. Please Try again.`;
            }

            if (!isLeapYear(Number(birthdayYear))) {
                if (birthdayDay === '29') {
                    throw `${birthdayMonth}/${birthdayDay}/${birthdayYear} is not a valid date since it is not a leap year. Please Try again.`;
                }
            }
        }

        // section converts birthdate to user age in total days
        const oneDay = 24 * 60 * 60 * 1000; // 24 hours, 60 minutes, 60 seconds, 1000 milliseconds = ms in one day
        let ageDiffInMs = Date.now() - fullBirthdate.getTime(); // today in ms - birthday in ms
        let ageDate = new Date(ageDiffInMs); // new date obj from age in ms calculation
        let ageInYears = Math.abs(ageDate.getUTCFullYear() - 1970); // utc year from age in ms - 1970 (epoch)
        let ageInDays = Math.floor(ageDiffInMs / oneDay); // age in ms / ms in one day = number of days since birth

        let height = Number(document.getElementById("heightInput").value);
        let weight = Number(document.getElementById("weightInput").value);

        // check height and weight entries for numeric values
        if (isNaN(height)) {
            throw "You must enter a valid, numeric, value for height.";
        }
        if (isNaN(weight)) {
            throw "You must enter a valid, numeric, value for weight.";
        }


        let gender;
        if (document.getElementById("maleSelected").checked) {
            gender = 2;
        } else if (document.getElementById("femaleSelected").checked) {
            gender = 1;
        }

        let systolic_bp = Number(document.getElementById("systolic_bp").value);
        let diastolic_bp = Number(document.getElementById("diastolic_bp").value);

        // check systolic and diastolic bp entries for numeric values
        if (isNaN(systolic_bp)) {
            throw "You must enter a valid, numeric, value for systolic blood pressure.";
        }
        if (isNaN(diastolic_bp)) {
            throw "You must enter a valid, numeric, value for diastolic blood pressure.";
        }

        let blood_glucose = document.getElementById("glucoseDropdownSelect").value;
        let cholesterol = document.getElementById("cholesterolDropdownSelect").value;

        let alcohol_intake;
        if (document.getElementById("yesAlcoholUse").checked) {
            alcohol_intake = 1;
        } else if (document.getElementById("noAlcoholUse").checked) {
            alcohol_intake = 0;
        }

        let current_smoker;
        if (document.getElementById("isASmoker").checked) {
            current_smoker = 1;
        } else if (document.getElementById("notASmoker").checked) {
            current_smoker = 0;
        }

        let physically_active;
        if (document.getElementById("yesActivity").checked) {
            physically_active = 1;
        } else if (document.getElementById("noActivity").checked) {
            physically_active = 0;
        }

        let allData = [
            {"age": ageInDays},
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

        if (ageInYears > 122) {
            allData.push({"pretty_old": ageInYears});
        }

        sendResults(allData)

    } catch(error) {
        alert(error);
        window.location.href = 'determine_risk'
    }
}

// Sends user input as an ajax post request to store as session data then send a get request to load the results page
function sendResults(data) {
    $.ajax({
        type: "POST",
        url: "/calculated_risk_results",
        dataType: "json",
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (data) {
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

function isLeapYear(year){
    return ((year % 4 === 0) && (year % 100 !== 0)) || (year % 400 === 0);
}