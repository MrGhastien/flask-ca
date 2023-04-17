//Hide date inputs when the corresponding checkboxes are not checked
const datechecks = document.getElementsByClassName('datecheck');
for (const check of datechecks) {
    const id = check.id;
    const dateinput = document.getElementById(`${id}-date`);
    dateinput.style.display = 'none';
    if (dateinput) {
        check.addEventListener('click', () => {
            if (check.checked)
                dateinput.style.display = 'inline-block';

            else
                dateinput.style.display = 'none';
            dateinput.required = check.checked;
        });
    }
}
