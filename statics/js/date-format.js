//Formatting dates
const texts = document.getElementsByClassName('format-date');
for (const t of texts) {
    const date = new Date(Date.parse(t.innerHTML));
    t.innerHTML = date.toLocaleString();
}