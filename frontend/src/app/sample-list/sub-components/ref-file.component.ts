import { Component, OnInit, Input } from '@angular/core';

import { RefFile } from '../../models/models';
import { ServerDataService } from '../../services/server-data.service';

@Component({
  selector: 'ref-file',
  template: `
    <p>
        {{ refFile.md5 }}
    </p>
  `
})

export class RefFileComponent implements OnInit {
  @Input() refFile: RefFile;
  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    // get data from server
  }
}
