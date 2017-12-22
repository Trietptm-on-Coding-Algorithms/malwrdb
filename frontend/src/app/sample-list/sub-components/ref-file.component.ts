import { Component, ViewChild, OnInit, Input } from '@angular/core';

import { ContextMenuModule, ContextMenuComponent } from 'ngx-contextmenu';

import { RefFile } from '../../models/models';
import { ServerDataService } from '../../services/server-data.service';

@Component({
  selector: 'ref-file',
  template: `
  <a href="" [contextMenu]="basicMenu">
      {{ refFile.file_name }}
  </a>

  <!-- RightClick menu to select actions -->
  <context-menu>
    <ng-template contextMenuItem (execute)="analyzeAsSample()">Analyze!</ng-template>
    <ng-template contextMenuItem (execute)="renameFile()">Rename</ng-template>
    <ng-template contextMenuItem (execute)="delFile()">Delete</ng-template>
  </context-menu>
  `
})

export class RefFileComponent implements OnInit {
  @Input() refFile: RefFile;
    @ViewChild(ContextMenuComponent) basicMenu: ContextMenuComponent;

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    // get data from server
  }

    analyzeAsSample(){
        console.log("analyze as sample");
    }

    renameFile(){
        console.log("rename file");
    }

    delFile(){
        console.log("del file");
    }
}
