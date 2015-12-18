input metauml

beginfig(1);
    Begin.b;
    Branch.pack;    % part of pack?
    % y:
        Activity.aPack("Analyse pack");
    % n:
        Activity.pEst("Determine Pitch");
    
    Activity.misP("Determine missing", "pitches");
    Activity.collSnd("Search similar sounds", "with specific pitch");
    Activity.mostFit("Pick most 'fit'", "sound");
    Branch.fitness; % fitness > th?
    % y:
        Activity.addSnd("Add to", "scale");
    % n:
        Branch.tries;   % tries < max_tries?
        % y: link back to collSnd
        % n:
            Activity.flag("Flag as missing", "pitch");
    Branch.allP;
        % n: link back to misP
        % y: 
            Branch.flaggedP; % any pitches flagged as missing?
            % y:
                Activity.pShift("Transform most fit", "neighbour of", "missing sounds");
                % link back to flagedP
            % n:
                End.e;

    topToBottom(20)(b, pack, pEst, misP, collSnd, tries);
    leftToRight(50)(pack, aPack);
    leftToRight(20)(collSnd, mostFit);
    topToBottom(20)(mostFit, fitness);
    topToBottom(20)(fitness, addSnd);
    topToBottom(20)(tries, flag);
    topToBottom(40)(addSnd, allP);
    topToBottom(40)(flag, flaggedP, e); 
    leftToRight(20)(pShift, flaggedP);

    drawObjects(b, pack, aPack, pEst, misP, collSnd, mostFit, fitness, addSnd, tries, flag, allP, flaggedP, pShift, e);

    clink(transition)(b, pack);
    clink(transition)(pack, aPack);
        item(iGuard)("part of pack")(obj.ne = aPack.n + (-50, 0));
    clink(transition)(pack, pEst);
        item(iGuard)("else")(obj.nw = pEst.n + (0, 20));
    clink(transition)(pEst, misP);
    clink(transition)(misP, collSnd);
        item(iGuard)("(needed pitch)")(obj.nw = misP.s + (0, -1));
    
    clink(transition)(collSnd, mostFit);
    clink(transition)(mostFit, fitness);
    clink(transition)(fitness, addSnd);
        item(iGuard)("fitness > th")(obj.nw = addSnd.n + (0, 20)); 
    clink(transition)(fitness, tries);
        item(iGuard)("else")(obj.nw = tries.e + (40, 10));
    link(transition)(pathStepX(tries.w, collSnd.w, -80));
        item(iGuard)("tries < max_tries")(obj.nw = collSnd.s + (-70, -15));
    clink(transition)(tries, flag);
        item(iGuard)("else")(obj.nw = flag.n + (0, 20)); 
    clink(transition)(flag, addSnd);
    clink(transition)(addSnd, allP);
  
    clink(transition)(allP, flaggedP); 
        item(iGuard)("all pitches searched")(obj.nw = flaggedP.e + (20, 10));
    link(transition)(pathStepX(allP.e, misP.e, 60));
        item(iGuard)("else")(obj.nw = allP.e + (20, 10));

    clink(transition)(flaggedP, pShift);
        item(iGuard)("else")(obj.nw = pShift.e + (6, 10));
    link(transition)(pathStepY(pShift.n, flaggedP.n, 10));
    clink(transition)(flaggedP, e);
        item(iGuard)("no pitches flagged as missing")(obj.nw = e.n + (0, 20)); 
    
endfig;
end
