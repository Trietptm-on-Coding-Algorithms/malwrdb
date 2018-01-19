import { Component, OnInit, Input } from '@angular/core';

import { MaterialComponentModule } from '../../modules/material-component.module';

import { PeSample, PeImportDllTable } from '../../models/models-pe';
import { ServerDataService } from '../../services/server-data.service';


@Component({
  selector: 'pe-import',
  template: `
  <h1>Pe Import</h1>
  `,
})
export class PeImportComponent implements OnInit {
  @Input() peSample: PeSample;

  importDllList: Array<PeImportDllTable>;

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    this._svrdata.getPeImportInfo(this.peSample._id).subscribe(
      v => {
          this.importDllList = v;
          console.log(v);
      });
  }
}
