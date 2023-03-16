document.onreadystatechange = () => {
  if (document.readyState == "interactive") {
    const allElements = document.querySelectorAll("*");
    for (let i = 0; i < allElements.length; i++) 
    {
      checkElement(allElements[i]);
    }
  }
}

function checkElement(element)
{
  const loader = document.querySelector("[data-loader]");
  const loaderProgressBar = document.querySelector("[data-loader-progress-bar]");
  const hiddenProgressBar = document.querySelector("[data-hidden-progress-bar]");
  const allElements = document.querySelectorAll("*");
  const step = 100 / allElements.length;

  if (element) {
    const nextProgressBarWidth = step + Number(hiddenProgressBar.value);
    hiddenProgressBar.value = nextProgressBarWidth;
    loaderProgressBar.style.width = `${nextProgressBarWidth}%`;
    if (getElementWidthInPercentages(loaderProgressBar) >= 100) {
      setTimeout(() => {
        loader.classList.add("fade-out");
      }, 400);
      setTimeout(() => {
        loader.classList.add("hide");
      }, 1000);
    }
  } else {
    checkElement(element);
  }
}

function getElementWidthInPercentages(element) {
  const elementWidth = element.style.width;
  const elementWidthPercentage = elementWidth.substring(0, elementWidth.length - 1);
  return Number(elementWidthPercentage);
}