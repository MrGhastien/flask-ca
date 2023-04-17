//Formatting dates
const texts = document.getElementsByClassName('format-date');
for (const t of texts) {
    //const date = new Date(Date.parse(t.innerHTML));
    const date = new Date(parseInt(t.innerHTML) * 1000);
    t.innerHTML = date.toLocaleString();
}