const cardImage = document.querySelector('.card-image');
const cardTitle = document.querySelector('.card-title');
const cardDesc = document.querySelector('.card-description');


const renderCard = () => {
  cardTitle.textContent = 'Card Title Yo!';
  cardDesc.textContent = 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Vero dicta repellat quibusdam assumenda at distinctio similique eos? Officiis voluptatem accusamus, id odit, quos eaque nemo, dicta quidem eum eligendi veritatis.';
  createImage();
  cardTitle.classList.remove('loading');
  cardDesc.classList.remove('loading');
  cardImage.classList.remove('loading');
};

function createImage() {
  const img = new Image();
  img.classList.add("image");
  img.setAttribute('alt', 'A cloud day at a mountain base');
  img.setAttribute('src', 'https://images.unsplash.com/photo-1516646255117-f9f933680173?ixlib=rb-0.3.5&q=85&fm=jpg&crop=entropy&cs=srgb&ixid=eyJhcHBfaWQiOjE0NTg5fQ&s=dc874984018a4253ba7d2a3c53387135');
  cardImage.appendChild(img);
}

setTimeout(() => {
  renderCard();
}, 5000);
