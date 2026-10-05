
document.querySelectorAll('[data-search]').forEach(input=>input.addEventListener('input',()=>{const q=input.value.trim().toLowerCase();document.querySelectorAll('[data-searchable]').forEach(el=>{el.hidden=q&&!el.textContent.toLowerCase().includes(q)})}));
document.querySelectorAll('a[href^="http"]').forEach(a=>{a.rel='noopener noreferrer';});
