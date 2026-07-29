document.addEventListener("DOMContentLoaded", function () {


const analyzeResumeBtn = document.getElementById(
    "analyzeResumeBtn"
);



if (!analyzeResumeBtn) {

    console.error(
        "Resume analyze button not found"
    );

    return;

}




analyzeResumeBtn.addEventListener(
"click",
async function () {



const fileInput = document.getElementById(
    "resumeFile"
);



const file = fileInput.files[0];



if (!file) {


alert(
    "Please upload your CV first."
);


return;


}




const allowedTypes = [

    "application/pdf",

    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

];



if (!allowedTypes.includes(file.type)) {


alert(
    "Only PDF or DOCX CV files are allowed."
);


return;


}




const formData = new FormData();



formData.append(
    "resume",
    file
);





const token = localStorage.getItem(
    "access"
);




if (!token) {


alert(
    "Your session expired. Please login again."
);


window.location.href = "/login/";


return;


}






const results = document.getElementById(
    "resumeResults"
);



results.innerHTML = `

<p>
⏳ Analyzing your CV...
</p>

`;





try {



const response = await fetch(

    "/api/ai/analyze-resume/",

    {

        method:"POST",


        headers:{

            "Authorization":
            `Bearer ${token}`

        },


        body:formData

    }

);






const data = await response.json();




console.log(
    "Resume Analysis:",
    data
);





if (!response.ok) {


throw new Error(

JSON.stringify(
    data,
    null,
    2
)

);


}






results.innerHTML = `


<div class="resume-card">


<h3>
📄 CV Analysis Result
</h3>



<h2>
Resume Quality Score:
${
data.resume_quality_score < 1
?
Math.round(data.resume_quality_score * 100)
:
Math.round(data.resume_quality_score)
}%
</h2>





<h4>
✅ Strengths
</h4>


<ul>

${
(data.strengths || [])
.map(
skill => `<li>${skill}</li>`
)
.join("")
}


</ul>





<h4>
⚠ Areas To Improve
</h4>


<ul>


${
(data.weaknesses || [])
.map(
item => `<li>${item}</li>`
)
.join("")
}


</ul>



<ul>


${
(data.missing_skills || [])
.map(
skill => `<li>${skill}</li>`
)
.join("")
}


</ul>





<h4>
💡 Recommendations
</h4>


<ul>


${
(data.recommendations || [])
.map(
item => `<li>${item}</li>`
)
.join("")
}


</ul>



</div>


`;





}

catch(error){



console.error(

"Resume Analyzer Error:",
error

);




results.innerHTML = `


<div class="error">


<h3>
❌ CV Analysis Failed
</h3>


<pre>
${error.message}
</pre>


</div>


`;



}



});


});