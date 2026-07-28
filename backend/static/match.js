const matchBtn =
document.getElementById("matchBtn");


if(matchBtn){

matchBtn.addEventListener(
"click",
async()=>{


const resume =
document.getElementById(
"matchResume"
).files[0];


const jobDescription =
document.getElementById(
"matchJobDescription"
).value;



const results =
document.getElementById(
"matchResults"
);



if(!resume || !jobDescription.trim()){

    results.innerHTML =
    "⚠ Upload resume and paste job description.";

    return;

}



const token =
localStorage.getItem("access");



const formData =
new FormData();



formData.append(
"resume",
resume
);


formData.append(
"job_description",
jobDescription
);



results.innerHTML =
"🤖 AI matching resume...";



const response =
await fetch(
"/api/matching/analyze/",
{

method:"POST",

headers:{

"Authorization":
`Bearer ${token}`

},

body:formData

}

);



const data =
await response.json();



if(!response.ok){

results.innerHTML =
JSON.stringify(data);

return;

}



results.innerHTML = `

<h3>
🎯 Match Score
</h3>

<h1>
${data.match_score}%
</h1>


<h3>
✅ Matching Skills
</h3>

<p>
${data.matching_skills.join(", ")}
</p>


<h3>
⚠ Missing Skills
</h3>

<p>
${data.missing_skills.join(", ")}
</p>


<h3>
🚀 Recommendation
</h3>

<p>
${data.recommendation}
</p>

`;



});

}