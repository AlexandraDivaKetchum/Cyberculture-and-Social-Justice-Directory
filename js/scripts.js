// Listen for click on the document
document.addEventListener('click', function (event) {

  var target = event.target
  //Bail if our clicked element doesn't have the class
  console.info(target.classList + target.parentElement.classList);
  if (!target.classList.contains('heading') && !target.parentElement.classList.contains('heading')) return;
  // Get the target content
  var article = target.closest('.article');
  var content = article.querySelector('.content')
  console.info(content);
  // var content = document.querySelector(target.hash);
  if (!content) return;

  // Prevent default link behavior
  event.preventDefault();

  // If the content is already expanded, collapse it and quit
  if (content.classList.contains('active')) {
    content.classList.remove('active');
    return;
  }

  // Get all open accordion content, loop through it, and close it
  // var accordions = document.querySelectorAll('.accordion-content.active');
  // for (var i = 0; i < accordions.length; i++) {
  //   accordions[i].classList.remove('active');
  // }

  // Toggle our content
  content.classList.toggle('active');
});
