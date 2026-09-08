# mir_eval PASS_TO_PASS after B2

- Exit code: 0
- Source: `fe73b3533737814f83dbd9739f06e90f5f82f758`

```text
xxxxxxxxxxxxxxxxxxxx............xxxxxxxxxxxxxxxxxx...................... [ 10%]
....xxxxxxx............xxxxxxx.......x.................x................ [ 20%]
........................................................................ [ 30%]
.....................................xxx................................ [ 40%]
....x........ss..x.....................xxxxxxxx.....xx.................. [ 50%]
xx....................................................................x. [ 60%]
..xxxxxx......................................xxx.................xxxxxx [ 70%]
xxxxxx...........xxxxxx........xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx [ 80%]
x..................................xxx........xxxxxxxxxxxxxxx........... [ 90%]
............xxxx......................x.........xxxxxxxxxxXxx.....       [100%]
=============================== warnings summary ===============================
tests/test_key.py: 58 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/key.py:165: UserWarning: The selected key scoring method does not match that currently used by MIREX. To use the same method, specify allow_descending_fifths=True. The default behaviour will change to allow_descending_fifths=True in the future.
    warnings.warn(

tests/test_multipitch.py: 10 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/multipitch.py:412: UserWarning: Estimate times not equal to reference times. Resampling to common time base.
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================ tests coverage ================================
______________ coverage: platform darwin, python 3.10.19-final-0 _______________

Name                                                                                                                                                Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/__init__.py                    18      0   100%
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/alignment.py                   75     21    72%   72, 77, 87, 94, 96, 104, 106, 110, 112, 226-247, 253
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/beat.py                       214      2    99%   524, 617
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/chord.py                      376      3    99%   195-196, 416
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/display.py                    418     88    79%   122-123, 247-249, 262-266, 276-279, 389-391, 424-427, 605-607, 617-621, 626-629, 638, 705-707, 736-739, 812-814, 822-825, 970-1043, 1244, 1260, 1267-1271, 1278, 1316-1324
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/hierarchy.py                  149      0   100%
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/io.py                         176     14    92%   432-445, 529, 536-537
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/key.py                         48      2    96%   181, 191
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/melody.py                     161     11    93%   104, 264, 296, 393, 398, 410-417, 435-436, 614, 682
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/multipitch.py                 110     15    86%   74, 76, 78, 80, 82, 84, 86, 88, 277-278, 284-285, 291, 324-325
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/onset.py                       23      0   100%
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/pattern.py                    153      2    99%   165, 478
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/segment.py                    249      5    98%   150, 569, 724, 762, 853
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/separation.py                 295    267     9%   78-128, 143, 206-256, 328-368, 432-503, 578-618, 627-640, 656-691, 698-735, 745-815, 823-827, 835-839, 847-849, 887-925
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/sonify.py                     110      1    99%   169
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/tempo.py                       36      0   100%
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/transcription.py              130      0   100%
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/transcription_velocity.py      49      0   100%
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/mir_eval/util.py                       252      5    98%   254, 311, 315, 954-960
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
TOTAL                                                                                                                                                3042    436    86%
Coverage XML written to file coverage.xml
535 passed, 3 skipped, 176 xfailed, 1 xpassed, 68 warnings in 40.36s

```
