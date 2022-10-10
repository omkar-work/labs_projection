def get_data_freemium(hosting_package_sold_per_year = 12500):
    revenue_share = 0.5

    price_monthly_devd_purchase = 2.05
    price_monthly_devd_renew = 2.05
    price_monthly_deving_purchase = 2
    price_monthly_deving_renew = 2
    price_yearly_devd_purchase = 1.74
    price_yearly_devd_renew = 1.74
    price_yearly_deving_purchase = 1.7
    price_yearly_deving_renew = 1.7

    perc_customer_in_devd_market = 0.49
    perc_mbx_on_monthly = 0.65

    
    yoy_hosting_growth = 0.1
    mom_hosting_growth = pow(1 + yoy_hosting_growth, 1/12)

    dom_per_hosting = 1.99
    mail_attach_per_domain = 0.33
    perc_free_to_paid_conversion = 0.025

    free_retain_1 = 0.7
    free_retain_2 = 0.8
    free_retain_next = 0.85

    monthly_retain_1 = 0.2
    monthly_retain_2 = 0.7
    monthly_retain_next = 0.85

    yearly_retain_1 = 0.7
    yearly_retain_2 = 0.8
    yearly_retain_next = 0.85


    mbx_per_domain_free = 1.92
    mbx_per_domain_monthly = 1.66
    mbx_per_domain_yearly = 1.55

    # calculate the following
    # FREE
    free_retain_1_per_month = pow(free_retain_1, 1/12)
    free_retain_2_per_month = pow(free_retain_2, 1/12)
    free_retain_next_per_month = pow(free_retain_next, 1/12)

    free_retain_per_month = [free_retain_1_per_month]*12 + [free_retain_2_per_month]*12 + [free_retain_next_per_month]*12
    free_retention_curve = [mbx_per_domain_free]
    for i in range(1, len(free_retain_per_month)):
        free_retention_curve.append(free_retention_curve[-1]*free_retain_per_month[i])

    # could be anything
    free_monetization_curve = [.3, .1, .08, .07, .06, .05, .04, .03, .02, .02, .0150, .0150, .0167, .0167, .0167, .0167, .0167, .0167, .0167, .0167, .0167, .0167, .0167, .0167]

    monetization_perc = [perc_free_to_paid_conversion*i for i in free_monetization_curve]


    #  MONTHLY
    monthly_retain_1_per_month = pow(monthly_retain_1, 1/11)
    monthly_retain_2_per_month = pow(monthly_retain_2, 1/12)
    monthly_retain_next_per_month = pow(monthly_retain_next, 1/12)

    monthly_retain_per_month = [1] + [monthly_retain_1_per_month]*11 + [monthly_retain_2_per_month]*12 + [monthly_retain_next_per_month]*12

    monthly_retention_expansion_curve = [mbx_per_domain_monthly]
    for i in range(1, len(monthly_retain_per_month)):
        monthly_retention_expansion_curve.append(monthly_retention_expansion_curve[-1]*monthly_retain_per_month[i])

    # YEARLY
    yearly_retain_1_per_month = pow(yearly_retain_1, 1/11)
    yearly_retain_2_per_month = pow(yearly_retain_2, 1/12)
    yearly_retain_next_per_month = pow(yearly_retain_next, 1/12)

    # keep it 100% for the whole year
    yearly_retain_per_month = [1]*12 + [yearly_retain_1] + [1]*11 + [yearly_retain_2]*11 + [yearly_retain_next] + [1]*11
    # Not sure how this was calculated
    # yearly_retain_per_month = [1.00000000000000000, 0.90736488595184800, 0.99981096579528500, 0.99938627500047700\
        # , 1.00086957848916000, 1.00542808422451000, 1.00284273586326000, 1.00065116488166000, 1.00439561150557000, 1.00428604410877000, 0.99013574965433000, 0.98654628717844400, 0.70000000000000000, 0.90736488595184800, 0.99981096579528500, 0.99938627500047700, 1.00086957848916000, 1.00542808422451000, 1.00284273586326000, 1.00065116488166000, 1.00439561150557000, 1.00428604410877000, 0.99013574965433000, 0.98654628717844400, 0.80000000000000000, 0.90736488595184800, 0.99981096579528500, 0.99938627500047700, 1.00086957848916000, 1.00542808422451000, 1.00284273586326000, 1.00065116488166000, 1.00439561150557000, 1.00428604410877000, 0.99013574965433000, 0.98654628717844400]

    yearly_retention_expansion_curve = [mbx_per_domain_yearly]
    for i in range(1, len(yearly_retain_per_month)):
        yearly_retention_expansion_curve.append(yearly_retention_expansion_curve[-1]*yearly_retain_per_month[i])


    # ---------------------------------
    # ---------------------------------
    base_dom_with_mbx_free = hosting_package_sold_per_year * dom_per_hosting * mail_attach_per_domain
    # print(base_dom_with_mbx_free)

    # ---------------------------------
    # ---------------------------------
    new_free_dom = []
    tot_paid_dom = []

    month_retain = [pow(free_retain_1, 1/12)]*12 + [pow(free_retain_2, 1/12)]*12 + [pow(free_retain_next, 1/12)]*12
    for i in range(len(month_retain)):
        mon_perc = monetization_perc[i] if i<len(monetization_perc) else 0
        if i==0:
            paid_dom = base_dom_with_mbx_free * mon_perc
            tot_paid_dom.append(paid_dom)
            new_free_dom.append(base_dom_with_mbx_free)

        else:
            base_dom_with_mbx_free = (base_dom_with_mbx_free - tot_paid_dom[-1]) * month_retain[i-1]
            new_free_dom.append(base_dom_with_mbx_free)
            paid_dom = base_dom_with_mbx_free * mon_perc
            tot_paid_dom.append(paid_dom)
            
    tot_paid_dom_monthly = [i*perc_mbx_on_monthly for i in tot_paid_dom]
    tot_paid_dom_yearly = [i*(1-perc_mbx_on_monthly) for i in tot_paid_dom]
    list(zip(map(round, new_free_dom), map(round, tot_paid_dom), map(round, tot_paid_dom_monthly), map(round, tot_paid_dom_yearly)))

    # ---------------------------------
    # ---------------------------------

    # MONTHLY DETAILS


    tot_paid_mbx_monthly = []
    for i in range(len(tot_paid_dom_monthly)):
        tot = 0
        for j in range(0, i+1):
            tot += tot_paid_dom_monthly[j]*monthly_retention_expansion_curve[i-j]
        tot_paid_mbx_monthly.append(tot)

    tot_paid_mbx_monthly_devd = [perc_customer_in_devd_market*i for i in tot_paid_mbx_monthly]
    tot_paid_mbx_monthly_deving = [(1-perc_customer_in_devd_market)*i for i in tot_paid_mbx_monthly]

    tot_rev_monthly_devd = [(price_monthly_devd_purchase if i==0 else price_monthly_devd_renew)*\
                            tot_paid_mbx_monthly_devd[i]\
                        for i in range(len(tot_paid_mbx_monthly_devd))]

    tot_rev_monthly_deving = [(price_monthly_deving_purchase if i==0 else price_monthly_deving_renew)*\
                            tot_paid_mbx_monthly_deving[i]\
                        for i in range(len(tot_paid_mbx_monthly_deving))]

    list(zip(map(round, tot_paid_mbx_monthly), map(round, tot_paid_mbx_monthly_devd), map(round, tot_paid_mbx_monthly_deving), tot_rev_monthly_devd, tot_rev_monthly_deving))



    # YEARLY DETAILS


    tot_paid_mbx_yearly = []
    for i in range(len(tot_paid_dom_yearly)):
        tot = 0
        for j in range(0, i+1):
            tot += tot_paid_dom_yearly[j]*yearly_retention_expansion_curve[i-j]
        tot_paid_mbx_yearly.append(tot)

    tot_paid_mbx_yearly_devd = [perc_customer_in_devd_market*i for i in tot_paid_mbx_yearly]
    tot_paid_mbx_yearly_deving = [(1-perc_customer_in_devd_market)*i for i in tot_paid_mbx_yearly]

    tot_rev_yearly_devd = [(price_yearly_devd_purchase if i==0 else price_yearly_devd_renew)*\
                            tot_paid_mbx_yearly_devd[i]\
                        for i in range(len(tot_paid_mbx_yearly_devd))]

    tot_rev_yearly_deving = [(price_yearly_deving_purchase if i==0 else price_yearly_deving_renew)*\
                            tot_paid_mbx_yearly_deving[i]\
                        for i in range(len(tot_paid_mbx_yearly_deving))]

    list(zip(map(round, tot_paid_mbx_yearly), map(round, tot_paid_mbx_yearly_devd), map(round, tot_paid_mbx_yearly_deving), tot_rev_yearly_devd, tot_rev_yearly_deving))


    data = []
    n = len(new_free_dom)
    for i in range(n):
        tmp = [i, round(new_free_dom[i]), round(tot_paid_dom[i]), \
            round(tot_paid_dom_monthly[i]), round(tot_paid_mbx_monthly[i]), \
            round(tot_paid_mbx_monthly_devd[i]), round(tot_paid_mbx_monthly_deving[i]), \
            round(tot_rev_monthly_devd[i]), round(tot_rev_monthly_deving[i]), \
            round(tot_paid_dom_yearly[i]), round(tot_paid_mbx_yearly[i]), \
            round(tot_paid_mbx_yearly_devd[i]), round(tot_paid_mbx_yearly_deving[i]), \
            round(tot_rev_yearly_devd[i]), round(tot_rev_yearly_deving[i])]
        data.append(tmp)
    return data
  
print("Hello World")
get_data_freemium
