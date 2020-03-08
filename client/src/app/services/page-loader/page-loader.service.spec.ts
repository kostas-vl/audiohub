import { TestBed, inject } from '@angular/core/testing';

import { PageLoaderService } from './page-loader.service';

describe('PageLoaderService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [PageLoaderService]
    });
  });

  it('should be created', inject([PageLoaderService], (service: PageLoaderService) => {
    expect(service).toBeTruthy();
  }));
});
