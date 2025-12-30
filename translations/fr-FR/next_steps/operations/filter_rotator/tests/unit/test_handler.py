import datetime

from filter_rotator_function import template_evaluation

def test_filter_expressions():
  secs_now = int(datetime.datetime.now().timestamp())
  res = template_evaluation.eval_template('INCLUDE ItemID WHERE Items.CREATION_TIMESTAMP > {{int(unixtime(now - timedelta_days(14)))}}')
  assert '{{' not in res and '}}' not in res
  secs = res.split(' ')[-1]
  assert secs.isdigit()
  assert (int(secs) - secs_now) < 2

def test_filter_name():
  today = datetime.datetime.now().strftime('%Y%m%d')
  res = template_evaluation.eval_template("include-recent-items-{{datetime_format(now,'%Y%m%d')}}")
  assert res.startswith('include-recent-items-')
  assert res.endswith(today)

def test_expression_basics():
  assert template_evaluation.eval_expression('1 == 1')
  assert not template_evaluation.eval_expression('1 > 1')
  assert template_evaluation.eval_expression('True == True')
  assert template_evaluation.eval_expression('False == False')
  assert not template_evaluation.eval_expression('True == False')
  assert template_evaluation.eval_expression('"personal" in "personalize"')

  assert template_evaluation.eval_expression("datetime_format(now,'%Y%m%d') == datetime_format(now,'%Y%m%d')")
  assert template_evaluation.eval_expression("datetime_format(now-timedelta_days(1),'%Y%m%d') < datetime_format(now,'%Y%m%d')")
  assert not template_evaluation.eval_expression("datetime_format(now-timedelta_days(1),'%Y%m%d') > datetime_format(now,'%Y%m%d')")

def test_filter_match():
  day_old = "starts_with(filter.name,'include-recent-items-') and int(end(filter.name,8)) < int(datetime_format(now - timedelta_days(1),'%Y%m%d'))"
  # Three days old
  filter = {
    'name': template_evaluation.eval_template("include-recent-items-{{datetime_format(now-timedelta_days(3),'%Y%m%d')}}")
  }
  match = template_evaluation.eval_expression(day_old, {'filter': filter})
  assert match

  # Two days old
  filter['name'] = template_evaluation.eval_template("include-recent-items-{{datetime_format(now-timedelta_days(2),'%Y%m%d')}}")
  match = template_evaluation.eval_expression(day_old, {'filter': filter})
  assert match

  # One day old
  filter['name'] = template_evaluation.eval_template("include-recent-items-{{datetime_format(now-timedelta_days(1),'%Y%m%d')}}")
  match = template_evaluation.eval_expression(day_old, {'filter': filter})
  assert not match

  # Same day
  filter['name'] = template_evaluation.eval_template("include-recent-items-{{datetime_format(now,'%Y%m%d')}}")
  match = template_evaluation.eval_expression(day_old, {'filter': filter})
  assert not match
