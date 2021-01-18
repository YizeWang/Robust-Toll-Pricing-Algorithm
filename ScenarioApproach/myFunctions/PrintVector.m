function [] = PrintVector(type, vector)

    fprintf(type);
    fprintf(': [');
    fprintf('%g, ', vector(1:end-1));
    fprintf('%g]\n', vector(end));
    
end