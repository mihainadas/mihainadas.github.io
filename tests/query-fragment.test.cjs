const test=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');const vm=require('node:vm');
const routes=JSON.parse(fs.readFileSync('redirect-map.json','utf8'));
test('all known routes preserve query and fragment without trusting the incoming path',()=>{
 for(const [route,target] of Object.entries(routes)){
  const file=route.replace(/^\//,'')+(route.endsWith('/')?'index.html':'');
  const script=fs.readFileSync(file,'utf8').match(/<script>([\s\S]*?)<\/script>/)[1];
  let actual;
  vm.runInNewContext(script,{window:{location:{pathname:'//other.example/',search:'?analytics=off&x=%23',hash:'#evidence',replace:url=>actual=url}}});
  assert.equal(actual,target+'?analytics=off&x=%23#evidence');
 }
});
