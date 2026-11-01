const fs=require('fs'),f=process.argv[2];const r=require('./transform.js')(fs.readFileSync(f,'utf8'));fs.writeFileSync(process.argv[3]||f,r.code);console.log(JSON.stringify(r.n));
