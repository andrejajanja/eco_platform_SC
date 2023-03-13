let count = document.querySelector("#sec");
async function fja(){
    let x = 5;
    while(x > 0){
        count.innerHTML = x;
        await new Promise(resolve => setTimeout(resolve, 1000));
        x--;
    }
    window.location.href =  "/events";
}
fja();