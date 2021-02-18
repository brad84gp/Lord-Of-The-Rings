
// let url = 'https://the-one-api.dev/v2/character'


// const pageNum = document.querySelectorAll('.page-num').forEach(pageNum => pageNum.addEventListener('click', function(e){
//     e.preventDefault()

//     const tables = document.getElementById('tables')

//     tables.removeChild

//     const targetPage = e.target.innerHTML
//     num = +targetPage
//     setPage(num)
// }))


// async function setPage(num){
//     await axios.get(url, {headers : {"Authorization": "Bearer SM2-H9EPKADRqF7VCURF"}})
//     .then(res => {
//         createTables(res.data.docs, num)
//     })
// }




// function createTables(data, num){

//     let counter = 0
//     let x = num
//     while(counter < 100) {
//         const tablesDiv = document.getElementById('tables')

//         const newDiv = document.createElement('div')
//         newDiv.classList.add('col')
//         newDiv.setAttribute('id', 'col')
//         tablesDiv.appendChild(newDiv)

//         const newCard = document.createElement('div')
//         newCard.classList.add('card')
//         newCard.style.height = '350px'
//         newDiv.appendChild(newCard)

//         const cardHeader = document.createElement('div')
//         cardHeader.classList.add('card-header')
//         cardHeader.innerText = data[x].name
//         newCard.appendChild(cardHeader)

//         const cardBody = document.createElement('div')
//         cardBody.classList.add('card-body')

//         cardHeader.appendChild(cardBody)

//         const cardText = document.createElement('p')
//         cardText.classList.add('card-text')
//         cardBody.appendChild(cardText)

//         const ul = document.createElement('ul')
//         cardText.appendChild(ul)
//         for(let i in data[x]){
//             if(i == 'name' || i == '_id'){
//                 continue
//             }else{
//                 const li = document.createElement('li')
//                 li.innerText = `${i} : ${data[x][i]}`
//                 ul.appendChild(li)
//             }
            
//         }
//         x++
//         counter++
//     }

// }

var exampleEl = document.getElementById('example')
var myPopoverTrigger = document.getElementById('myPopover')
myPopoverTrigger.addEventListener('show.bs.popover', function () {
    console.log('works')
})
// var newPopperConfig = {...}
// use defaultBsPopperConfig if needed...
// return newPopperConfig


