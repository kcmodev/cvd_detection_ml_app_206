// function loginButton() {
//     location.href = '/data'
// }


document.getElementById("submitDataButton").onclick = function submitUserInput() {
    // alert('button clicked test')
    let userAgeInDays;
    let todaysDateDays
    let bday = document.getElementById("ageInput").value;

    try {
        bday = Date.parse(bday);
        bday = (bday / (60*60*24*1000));
        console.log(`bday days since epoch: ${bday}`)

        todaysDateDays = Date.now();
        todaysDateDays = (todaysDateDays / (60*60*24*1000));
        console.log(`today's days since epoch: ${todaysDateDays}`)

        userAgeInDays = todaysDateDays - bday;

        // throws an error if the date format is invalid
        if (isNaN(userAgeInDays)){
            throw RangeError;
        }

    }
    catch (RangeError){
        alert('Birthday date format invalid')
    }

    let height = document.getElementById("heightInput").value;
    let weight = document.getElementById("weightInput").value;

    let gender = document.getElementsByName("gender");
    if (gender[0].checked) {
        gender = 1;
    }
    if (gender[1].checked) {
        gender = 0;
    }
    
    let sbp = document.getElementById("systolic_bp").value;
    let dbp = document.getElementById("diastolic_bp").value;
    let gluc = document.getElementById("glucoseDropdownSelect").value;
    let chol = document.getElementById("cholesterolDropdownSelect").value;
    let alch = document.getElementById("alcoholRadioButtonGroup").value;
    let phys = document.getElementById("activityRadioButtonGroup").value;

    console.log(`testing values - age in days: ${userAgeInDays}, ht: ${height}, wgt: ${weight}, gender: ${gender},
    bp: ${sbp}/${dbp}, gluc: ${gluc}, chol: ${chol}, alch: ${alch}, phys: ${phys}`);
};
