window.onload = function () {
    document.getElementById("download")
        .addEventListener("click", () => {
            const table = this.document.getElementById("reconciliation-table");
            
            let today = new Date().toISOString().slice(0, 10)
            var opt = {
                margin: 1,
                filename: 'inventory-'+today+'.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                jsPDF: { unit: 'in', format: 'letter', orientation: 'landscape' }
            };
            
            html2pdf().from(table).set(opt).save();
        })
}