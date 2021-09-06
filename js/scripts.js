// Listen for click on the document
document.addEventListener('click', function (event) {

  var target = event.target
  //Bail if our clicked element doesn't have the class
  if (!target.classList.contains('heading') && !target.parentElement.classList.contains('heading')) return;

  // Get the target content
  var article = target.closest('.article');
  var content = article.querySelector('.content')
  if (!content) return;

  // Prevent default link behavior
  event.preventDefault();

  // If the content is already expanded, collapse it and quit
  if (content.classList.contains('active')) {
    content.classList.remove('active');
    return;
  }

  // Toggle our content
  content.classList.toggle('active');
});
