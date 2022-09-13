let containerr = document.getElementById('containerr')
        for (let i = 1; i < 65; i++) {
            let elm = document.createElement('button')
            elm.className = "btn"
             elm.id = "btnid"
            containerr.appendChild(elm)
            // document.getElementById('btnid').style.backgroundColor = "black"
        }
var a = 1;
var price = 100;
var haj ;

        for(let i=0;i<document.getElementsByTagName("button").length;i++)
        {
            document.getElementsByTagName("button")[i].addEventListener("click", function () {
                document.getElementsByTagName('button')[i].style.backgroundColor = "black"
                var count = document.getElementById('count')
                 haj = `${a * price}`
                count.innerHTML = `you have selected <b style="color:teal">${a}</b> seats for a price of <b style="color:teal">$${haj}</b>`
                a++
            })

            document.getElementsByTagName("button")[i].addEventListener("dblclick", function () {
                a--
                document.getElementsByTagName('button')[i].style.backgroundColor = "white"
                haj = `${a * price / price /a}`
                count.innerHTML = `you have selected <b style="color:teal">${a}</b> seats for a price of <b style="color:teal">$${haj}</b>`
               
            })

        }

        // for(let i=0;i<document.getElementsByTagName("button").length;i++)
        // document.getElementsByTagName("button")[i].addEventListener("dblclick", function () {
        //     document.getElementsByTagName('button')[i].style.backgroundColor = "black"
        //     var count = document.getElementById('count')
        //     var haj = `${a * price /price}`
        //     count.innerHTML = `you have selected ${a} seats for a price of ${haj}`
        //     a--
        // },{once:true})