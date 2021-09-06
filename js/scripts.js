const searchBar = document.getElementById('searchbar');

document.addEventListener('click', function (event) {
  const target = event.target;
  if (target.classList.contains('heading') || target.parentElement.classList.contains('heading')) {
    toggleArticleContent(target);
    return;
  }

  if (target.nodeName === 'LABEL') {
    onTagClicked(target);
  }
});

function onTagClicked(element) {
  searchBar.value = element.innerHTML.toLowerCase();
  searchTags();
}

function toggleArticleContent(element) {
  const article = element.closest('article');
  const content = article.querySelector('.content');

  if (!content) return;

  if (content.classList.contains('active')) {
    content.classList.remove('active');
    return;
  }
  content.classList.add('active');
}


function searchTags() {
  const input = searchBar.value.toLowerCase();


  // Reset the hidden articles
  document.querySelectorAll('article.hidden').forEach((article) => {
    article.classList.remove('hidden');
  });

  if (!input || input === '') return;

  document.querySelectorAll('.tags').forEach((tagContainer) => {
    const tags = Array.from(tagContainer.querySelectorAll('label')).map(
        (tag) => tag.innerHTML.toLowerCase()
    );
    if (!tags.includes(input)) {
      tagContainer.closest('article').classList.add('hidden');
    }
  });
}
