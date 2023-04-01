const element = document.getElementById('post-text');
const innerHTML = element.innerHTML;
const formattedText = innerHTML.replace(/\n/g, '<br>');
document.getElementById('post-text').innerHTML = formattedText;