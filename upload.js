const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');
const recursive = require('recursive-fs');
const basePathConverter = require('base-path-converter');

const pinDirectoryToIPFSJson = (pinataApiKey, pinataSecretApiKey) => {
    const url = `https://api.pinata.cloud/pinning/pinFileToIPFS`;
    const src = './build/Json';

    //we gather the files from a local directory in this example, but a valid readStream is all that's needed for each file in the directory.
    recursive.readdirr(src, function (err, dirs, files) {
        let data = new FormData();
        files.forEach((file) => {
            //for each file stream, we need to include the correct relative file path
            data.append(`file`, fs.createReadStream(file), {
                filepath: basePathConverter(src, file)
            });
        });

        const metadata = JSON.stringify({
            name: 'Json',
            keyvalues: {
                exampleKey: 'exampleValue'
            }
        });
        data.append('pinataMetadata', metadata);

        return axios
            .post(url, data, {
                maxBodyLength: 'Infinity', //this is needed to prevent axios from erroring out with large directories
                headers: {
                    'Content-Type': `multipart/form-data; boundary=${data._boundary}`,
                    pinata_api_key: pinataApiKey,
                    pinata_secret_api_key: pinataSecretApiKey
                }
            })
            .then(async function(response) {
                console.log(response.data['IpfsHash'])
                const res=await axios.get('http://127.0.0.1:8000/api/getClickUp')
                const res1 =await axios.post('http://127.0.0.1:8000/api/saveJsonCID/',{jsonCid:response.data['IpfsHash'],img:res.data},{
                headers:{
                    'Content-Type':'application/json'
                }});

                console.log("Json CID to:", res1.data);



            })
            .catch(function (error) {
                console.log(error)
            });
    });
};



pinDirectoryToIPFSJson('32bb4d3965c227938873','5f329f7eaa3922292de5d0c03a76b2ee0bf25f21052680f7b68a2089fc3113b8')
