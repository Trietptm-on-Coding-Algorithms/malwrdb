import { Component, OnInit, Input } from '@angular/core';

import { MaterialComponentModule } from '../../modules/material-component.module';

import { PeSample, PeValueStructure } from '../../models/models-pe';
import { ServerDataService } from '../../services/server-data.service';


@Component({
  selector: 'pe-header',
  template: `
  <h1>Pe Header</h1>
  <p *ngFor="let v of dosHeader">
    <span>{{v.name}}</span>
    <br/>
  </p>
  `,
})
export class PeHeaderComponent implements OnInit {
  @Input() peSample: PeSample;

  dosHeader: Array<PeValueStructure>;
  fileHeader: Array<PeValueStructure>;
  ntHeader: Array<PeValueStructure>;

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    console.log(this.peSample);
    this._svrdata.getPeHeaderInfo(this.peSample._id).subscribe(
      v => {
        this.dosHeader = v["dos_header"];
        this.fileHeader = v["file_header"];
        this.ntHeader = v["nt_header"];
      },
      e => {
        console.log(e);
      }
    );
  }
}
