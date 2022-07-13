window.onload = function () {
    document.getElementById("download")
        .addEventListener("click", () => {
            const receipt = this.document.getElementById("receipt");
            
            let name = document.getElementsByClassName('title')[0].innerText
            var opt = {
                margin: 1,
                filename: name+'.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                jsPDF: { unit: 'in', format: 'letter', orientation: 'landscape' }
            };
            
            html2pdf().from(receipt).set(opt).save();
        })
}