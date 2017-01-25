import datetime
import grants


if __name__ == '__main__':
    today = datetime.date.today()
    for award in grants.parse():
        if award.first_vesting_date > today:
            print('*FIRST VESTING* Your %s award of %d shares will vest %d shares on %s!' % (award.commencement_date,
                  award.shares, (award.shares//award.vesting_schedule_in_years),
                  award.first_vesting_date))
