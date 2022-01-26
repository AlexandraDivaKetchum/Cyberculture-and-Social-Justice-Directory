const searchBar = document.getElementById('searchBar');
const keyWords = document.querySelector('meta[name="keywords"]').content;
const keyWordList = keyWords.split(",");

document.addEventListener('click', function (event) {
  const target = event.target;
  if (target.classList?.contains('heading') || target.parentElement?.classList?.contains('heading')) {
    toggleArticleContent(target);
    return;
  }

  if (target.nodeName === 'LABEL') {
    onTagClicked(target);
  }
});


searchBar.addEventListener('keyup', function (event) {
  if (event.key === 'Enter' || event.keyCode === 13) {
    searchTags();
  }
});

const autoCompleteJS = new autoComplete({
  selector: "#searchBar",
  placeHolder: "Search tags...",
  data: {
      src: keyWordList,
      cache: true,
  },
  resultsList: {
      element: (list, data) => {
          if (!data.results.length) {
              // Create "No Results" message element
              const message = document.createElement("div");
              // Add class to the created element
              message.setAttribute("class", "no_result");
              // Add message text content
              message.innerHTML = `<span>Found No Results for "${data.query}"</span>`;
              // Append message element to the results list
              list.prepend(message);
          }
      },
      noResults: true,
  },
  resultItem: {
      highlight: true
  },
  events: {
      input: {
          selection: (event) => {
              const selection = event.detail.selection.value;
              autoCompleteJS.input.value = selection;
              searchTags();
          }
      }
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
