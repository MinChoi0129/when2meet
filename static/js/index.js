class Index {
    constructor() {
        console.log("ehla?")
        this.clickGroupIn();
        this.clickCloseGroupin();
        this.clickGroupMake();
        this.clickCloseGroupMake()
    }


    /* groupin.html x 클릭 이벤트 */
    clickCloseGroupin(){
        let closeBtn = document.querySelectorAll('.closeBtn')
        closeBtn[2].addEventListener('click',()=>{
            document.querySelector('.groupinModal').classList.add('unactive')

        })
    }

    /* groupin.html 그룹 참가 클릭 이벤트 */
    clickGroupIn(){
        const groupinBtn = document.querySelector('.join')
        groupinBtn.addEventListener('click',()=>{
            document.querySelector('.groupinModal').classList.remove('unactive')
        })
        console.log("hirerererer")
    }

    
    /* groupmake.html x 클릭 이벤트 */
    clickCloseGroupMake(){
        let closeBtn = document.querySelectorAll('.closeBtn')
        closeBtn[3].addEventListener('click',()=>{
            document.querySelector('.groupmakeModal').classList.add('unactive')

        })
    }

    /* groupmake.html 그룹 참가 클릭 이벤트 */
    clickGroupMake(){
        const groupinBtn = document.querySelector('.make')
        groupinBtn.addEventListener('click',()=>{
            document.querySelector('.groupmakeModal').classList.remove('unactive')
        })
    }
    slider(){
        const dots = document.querySelectorAll('.sumnail ul li')

        const next = () => {
            if (current >= images.length - 1) return;
            slider.style.transition = '400ms ease-in-out transform';
            current++;
            slider.style.transform = `translateX(${-imgSize * current}px)`;
        
            for (let i = 0; i < dots.length; i++) {
                if (dots[i].dataset.index == current) {
                    dots[i].classList.add('active');
                } else if (current === 4) {
                    dots[i].classList.remove('active');
                    dots[0].classList.add('active');
                }
                else {
                    dots[i].classList.remove('active');
                }
            }
        }
        
        setInterval(next, 2000);
        console.log("잘도미")

    }

}
window.onload = () => {
    new Index();
};
