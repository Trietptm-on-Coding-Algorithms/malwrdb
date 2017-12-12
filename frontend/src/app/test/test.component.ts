import { Component, OnInit } from '@angular/core';
import { DataContextService } from '../services/datacontext.service'

@Component({
  selector: 'test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit {

  data: any;

  constructor(private _dtctx: DataContextService) { }

  ngOnInit() {
  }

  doTest(): void {
    console.log("xxxxxxxxxx")
  	// this.data = this._dtctx.getTestData()
    //const testFolder = './tests/';
    //const fs = require('fs');
//
    //fs.readdir(testFolder, (err, files) => {
    //  files.forEach(file => {
    //    console.log(file);
    //  });
  }

}
