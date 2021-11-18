import {sync} from 'glob';
import {join} from 'path';

let root: string = '/Users/djptek/github/kibana/x-pack/plugins/';
//let matcher: string = '**/*.ts';
let matcher: string = '**/span_flyout.stories.tsx';
let target: string = join(root, matcher);

console.log("looking for %s", target);

// interested in *.ts, *.tsx, *.json, *.tsx.snap

let filePaths: string[] = sync(target);

console.log("found %d files", filePaths.length);

for (let filename of filePaths) {
  console.log(filename);
}