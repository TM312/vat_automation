// import Vue from 'vue'
// var fs = require('fs')

// Vue.use(fs)





// axios({
//     url: 'http://api.dev/file-download',
//     method: 'GET',
//     responseType: 'blob', // important
// }).then((response) => {
//     const url = window.URL.createObjectURL(new Blob([response.data]));
//     const link = document.createElement('a');
//     link.href = url;
//     link.setAttribute('download', 'file.pdf'); //or any other extension
//     document.body.appendChild(link);
//     link.click();
// });


// onClick() {



// "/download/<string:activity_period>/<string:filename>"

//     axios({
//         method: 'GET',
//         url: '/api',
//         params: params,
//         responseType: 'blob'
//     }).then(res => {
//         const blob = new Blob([response.data], { type: response.data.type });
//         let url = window.URL.createObjectURL(blob);
//         window.location.href = url;
//         const contentDisposition = response.headers['content-disposition'];
//         let fileName = 'unknown';
//         if (contentDisposition) {
//             const fileNameMatch = contentDisposition.match(/filename="(.+)"/);
//             if (fileNameMatch.length === 2)
//                 fileName = fileNameMatch[1];
//         }
//         link.setAttribute('download', fileName);

//         document.body.appendChild(link);
//         link.click();
//         link.remove();

//         window.URL.revokeObjectURL(url);
//     }).catch(err => {
//         console.log(err)
//     })

// }
